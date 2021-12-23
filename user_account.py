import logging
import os
from hashlib import sha3_256
from re import compile
import file_handling
from datetime import datetime, timedelta

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

    def __init__(self, username, password):
        self.username = username
        self.__password = password
        self.locking = False

    def register(self):
        """
        for each user ,username and password must be saved in file
        if his/her username not exist, he/she can sign up .
        information_list >> a list of dictionaries of 'username and password(hashing)' of each user
        information_list = [{'username':...,'password(hash)':...},...]
        """
        my_file = file_handling.File('users_information.csv')
        if os.path.exists('users_information.csv'):
            information_list = my_file.read_csvfile_as_dictionary()
        else:
            my_file.write({'username': '', 'password': ''})
            information_list = []

        if information_list:
            usernames_list = []
            for item in information_list:
                usernames_list.append(item['username'])

            if self.username not in usernames_list:

                info = {'username': self.username, 'password': User.hash_method(self.__password)}
                my_file.write(info)
                logger.info(f" new person with username: {self.username},registered into program")
            else:
                logging.warning("this username isn't available.try Again...")
        else:
            info = {'username': self.username, 'password': User.hash_method(self.__password)}
            my_file.write(info)
            logger.info(f" new person with username: {self.username},registered into program")

    @staticmethod
    def get_users_info_list():
        # returns a list of tuples >> [(username,password)]
        users_info_list = []
        my_file = file_handling.File('users_information.csv')
        information_list = my_file.read_csvfile_as_dictionary()
        for item in information_list:
            users_info_list.append((item['username'], item['password']))
        return users_info_list

    def login(self):
        # if the username and password is correct,the user can log in .
        info_list = User.get_users_info_list()
        # usernames list
        users_list = []
        # password list
        password_list = []
        for item in info_list:
            if item:
                users_list.append(item[0])
                password_list.append(item[1])
        if self.username not in users_list:
            logger.error('this username not exist!')
        else:
            for i in range(len(users_list)):
                if users_list[i] == self.username:
                    if password_list[i] == User.hash_method(self.__password):
                        print(f'You:{self.username} have successfully entered the program :)')
                        logger.info(f'"{self.username}" have successfully entered the program ')
                    else:
                        logger.error('the password is not correct.try again')
                        # for 3 time can repeat the password and if can't entry true
                        # password this account must be locked.
                        # calling locking_account method

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
        # if a user entry incorrect password for 3 time then his/her account
        # locked for one hour
        self.locking = True
        now = datetime.now()
        unlocking_account = now + timedelta(hours=1)
        if datetime.now() >= unlocking_account:
            self.locking = False
        return self.locking

    def creating_folders_for_each_user(self):
        """
        Creates a folder for each user called the username of that user and
        inside that folder, creates three more folders for Inbox and Sent and Draft.
        """
        os.makedirs(f'{self.username}\\Inbox')
        os.makedirs(f'{self.username}\\Draft')
        os.makedirs(f'{self.username}\\Sent')

    def __repr__(self):
        return f'username: {self.username},password(hashing): {User.hash_method(self.__password)}'

