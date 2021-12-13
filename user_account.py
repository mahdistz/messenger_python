import logging
import re
import hashlib
import file_handler_module


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('user.log')
file_handler.setLevel(level=logging.INFO)

# create formatters and add it to handlers

file_format = logging.Formatter('%(asctime)s ::%(levelname)s - %(filename)s - %(message)s')
file_handler.setFormatter(file_format)

# add handlers to the logger
logger.addHandler(file_handler)


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def sign_up(self):
        # if his/her username not exist, he/she can sign up .
        logger.info('a new person singed up into program')
        return " register a person into program"

    def sign_in(self):
        # if the username and password is correct,the user can sign in .
        logger.info('an user was signed in program ')
        return "sign in a person into program"

    def validation_password(self):
        if self.password:
            pass

    def validation_username(self):
        if self.username:
            pass

    def check_username_with_password(self):
        pass
