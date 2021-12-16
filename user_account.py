import logging
from hashlib import sha3_256
from re import compile
import file_handling

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(level=logging.WARNING)
file_handler = logging.FileHandler('user.log')
file_handler.setLevel(level=logging.INFO)

# create formatters and add it to handlers

stream_format = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
file_format = logging.Formatter('%(asctime)s ::%(levelname)s - %(filename)s - %(message)s')
stream_handler.setFormatter(stream_format)
file_handler.setFormatter(file_format)

# add handlers to the logger

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

PASSWORD_REGEX = compile(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,12}\Z')
USERNAME_REGEX = compile(r'\A[\w\-\.]{3,12}\Z')


class User:


    users_info_list = []

    def __init__(self, username, password):
        self.username = username
        self.__password = password

    def register(self):
        # for each user ,username and password must be saved in file
        # if his/her username not exist, he/she can sign up .
        # information_list = [{'key':'value'},...]
        my_file = file_handling.File('users_information.csv')
        information_list = my_file.read_csvfile_as_dictionary()
        usernames_list = []
        for item in information_list:
            usernames_list.append(item['username'])
        if self.username not in usernames_list:

            info = {'username': self.username, 'password': User.hash_method(self.__password)}
            file_handling.File('users_information.csv').write(info)
            logger.info(f" new person with username: {self.username},registered into program")
        else:
            logging.warning("this username isn't available")

    @staticmethod
    def get_users_info_list():
        # a list of tuples >> [(username,password)]
        my_file = file_handling.File('users_information.csv')
        information_list = my_file.read_csvfile_as_dictionary()
        for item in information_list:
            User.users_info_list.append((item['username'], item['password']))
        return User.users_info_list

    def login(self):
        # if the username and password is correct,the user can log in .
        info_list = User.get_users_info_list()
        users_list = []
        password_list = []
        for i in info_list:
            users_list.append(i[0])
            password_list.append(i[1])
        if self.username not in users_list:
            logger.error('this username not exist!')
        else:
            for i in range(len(users_list)):
                if users_list[i] == self.username:
                    if password_list[i] == User.hash_method(self.__password):
                        print(f'You:{self.username} have successfully entered the program :)')
                        logger.info(f'You:{self.username} have successfully entered the program :) ')
                    else:
                        logger.error('the password is not correct.try again')

    def validation_password(self):
        # Password must be 6 to 12 characters, 1 lowercase letter
        # 1 uppercase letter,1 digit
        return PASSWORD_REGEX.match(self.__password) is not None

    def validation_username(self):
        # username must be 3 to 12 characters and can include
        # letters,numbers and "-" ,"." ,"_"
        return USERNAME_REGEX.match(self.username) is not None

    @staticmethod
    def hash_method(obj):
        obj_hashing = sha3_256(obj.encode('ascii')).hexdigest()
        return obj_hashing

    def locking_account(self):
        return f"an user: {self.username} locked because entire incorrect password 3 time"

    def __repr__(self):
        return f'username: {self.username},password(hashing): {User.hash_method(self.__password)}'

