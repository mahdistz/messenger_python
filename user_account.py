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
        # for each user ,username and password must be saved in file.
        # if his/her username not exist, he/she can sign up . >> logger.error !

        logger.info(f" new person with username: {self.username},registered into program")
        return f"an user with username {self.username} registered."

    def login(self):
        # if the username and password is correct,the user can sign in .
        logger.info(f'an user with username {self.username} was signed in program ')
        return f"sign in an person with username {self.username} into program"

    def validation_password(self):
        """   Password must be
            - 6 chars or more
            - 1 lowercase letter
            - 1 uppercase letter
            - 1 digit
        """
        return PASSWORD_REGEX.match(self.__password) is not None

    def validation_username(self):
        return USERNAME_REGEX.match(self.username) is not None

    def check_username_with_password(self):
        pass

    @staticmethod
    def hash_method(obj):
        obj_hashing = sha3_256(obj.encode('ascii')).hexdigest()
        return obj_hashing

    def __repr__(self):
        return f'username: {self.username},password(hashing): {User.hash_method(self.__password)}'
