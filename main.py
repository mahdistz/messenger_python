import user_account
import working_in_messenger
import file_handling
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(level=logging.WARNING)
file_handler = logging.FileHandler('user.log')
file_handler.setLevel(level=logging.INFO)

# create formatters and add it to handlers

stream_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s ::%(levelname)s - %(filename)s - %(message)s')
stream_handler.setFormatter(stream_format)
file_handler.setFormatter(file_format)

# add handlers to the logger

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def checking_for_register(username, password):

    validation = False
    an_user = user_account.User(username, password)
    if an_user.validation_username():
        print(f'this username {username} is correct')
        if an_user.validation_password():
            again_password = input('repeat password : ')
            if password == again_password:
                print('you successfully added to Messenger.')
                validation = True
            else:
                logger.error('The password you entered does not match the default password.')
        else:
            print('the password is not correct!')
    else:
        logger.info('this username is not correct! please try again...')

    return validation


"""
Menu
"""

while True:
    try:
        my_input = input('Welcome to Messenger.Do you have an Account?(y/n): ').lower()
        if my_input == 'y':
            username_input = input('Enter username: ')
            password_input = input('Enter password: ')
            an_user1 = user_account.User(username_input, password_input).login()

        elif my_input == 'n':

            creating_account = input('Do You Want Sign up?(y/n): ').lower()
            if creating_account == 'y':

                print('username must be 3 to 12 characters and can include letters,numbers and "-" ,"." ,"_" ')
                print("Password must be 6 to 12 characters,1 lowercase letter,1 uppercase letter,1 digit")

                username_input1 = input('Enter username: ')
                password_input1 = input('Enter password: ')

                validation_register = checking_for_register(username_input1, password_input1)
                # validation_register >> A Boolean : True / False
                if validation_register:
                    user = user_account.User(username_input1, password_input1)
                    user.register()
                else:
                    continue

            elif creating_account == 'n':
                wanting_quit = input('Do You Want Quit?(y/n): ').lower()
                if wanting_quit == 'y':
                    break
                elif wanting_quit == 'n':
                    continue
                else:
                    raise ValueError('you should enter y or n')
            else:
                raise ValueError('you should enter y or n')
        else:
            raise ValueError('you should enter y or n')

    except (ValueError, TypeError) as error:
        logger.error('an exception occurred', exc_info=True)

    except Exception as error:
        logger.error('an exception occurred', exc_info=True)
