import logging
from hashlib import sha3_256
from re import compile
import file_handling

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(level=logging.INFO)
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
        """
        a list of tuples >> [(username,password)]
        """
        my_file = file_handling.File('users_information.csv')
        information_list = my_file.read_csvfile_as_dictionary()
        users_list = []
        for item in information_list:
            users_list.append((item['username'], item['password']))
        return users_list

    def login(self):
        # if the username and password is correct,the user can sign in .

        info_list = User.get_users_info_list()
        usernames_list = info_list[0]
        print(usernames_list)

        if self.username not in usernames_list:
            logger.error('this username not exist!')
        else:
            for item in info_list:
                if item[self.username] == User.hash_method(self.__password):
                    logger.info(f'You: {self.username} have successfully entered the program :) ')
                else:
                    logger.error('the password is not correct.try again')
        return "sign in a person into program"

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

    def check_hash_items(self, password1):
        password1 = User.hash_method(password1)
        password = User.hash_method(self.__password)
        if password1 == password:
            return True
        return False

    def __repr__(self):
        return f'username: {self.username},password(hashing): {User.hash_method(self.__password)}'
