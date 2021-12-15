import user_account
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('main.log')
file_handler.setLevel(level=logging.INFO)

# create formatters and add it to handlers

file_format = logging.Formatter('%(asctime)s ::%(levelname)s - %(filename)s - %(message)s')
file_handler.setFormatter(file_format)

# add handlers to the logger
logger.addHandler(file_handler)

"""
register
"""
# An user register in messenger

user_name = input("Enter username: ")
user_password = input("Enter password: ")

# if username is unique in this program and username and password patterns is correct
# then can be registered

user_defined_username = user_account.User(user_name, user_password).validation_username()
user_defined_password = user_account.User(user_name, user_password).validation_password()

if user_defined_password and user_defined_username:
    user_account.User(user_name, user_password).register()

"""
login
"""
