import user_account
import working_in_messenger
import file_handling
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(level=logging.INFO)
file_handler = logging.FileHandler('user.log')
file_handler.setLevel(level=logging.WARNING)

# create formatters and add it to handlers

stream_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s ::%(levelname)s - %(filename)s - %(message)s')
stream_handler.setFormatter(stream_format)
file_handler.setFormatter(file_format)

# add handlers to the logger

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def get_item_for_register():
    validation = False
    print('username must be 3 to 12 characters and can include letters,numbers and "-" ,"." ,"_" ')
    print("Password must be 6 to 12 characters,1 lowercase letter,1 uppercase letter,1 digit")
    username_input1 = input('Enter username: ')
    password_input1 = input('Enter password: ')
    an_user = user_account.User(username_input1, password_input1)
    if an_user.validation_username():
        logger.info(f'this username {username_input1} is correct')
        if an_user.validation_password():
            again_password = input('repeat password : ')
            if password_input1 == again_password:
                print('you successfully added to Messenger.')
                validation = True
            else:
                logger.error('The password you entered does not match the default password.')
                print('You can try up to 3 times')
                for i in range(3):
                    again_password_2 = input('repeat password : ')
                    if again_password_2 == password_input1:
                        print('you successfully added to Messenger.')
                        validation = True
                    else:
                        print('sorry you can not try anymore! ')
                        break
    else:
        logger.info('this username is not correct! please try again...')

    return validation, username_input1, password_input1


"""
Menu
"""

while True:
    try:
        my_input = input('Welcome to Messenger.Do you have an Account?(y/n): ').lower()
        if my_input == 'y':
            username_input = input('Enter username: ')
            password_input = input('Enter password: ')
            an_user1 = user_account.User(username_input, password_input)
            an_user1.login()

        elif my_input == 'n':

            creating_account = input('Do You Want Sign up?(y/n): ').lower()
            if creating_account == 'y':
                items_tuple = get_item_for_register()
                # item_tuple = (True/False, username , password)
                if items_tuple[0]:
                    user = user_account.User(items_tuple[1], items_tuple[2])
                    user.register()
                    # print(user)
            elif creating_account == 'n':
                wanting_quit = input('Do You Want Quit?(y/n): ').lower()
                if wanting_quit == 'y':
                    break
                elif wanting_quit == 'n':
                    continue
                else:
                    logger.error('you should enter y or n')
            else:
                logger.error('you should enter y or n')
        else:
            logger.error('you should enter y or n')

    except (ValueError, TypeError) as error:
        logger.error('an exception occurred', exc_info=True)

    except Exception as error:
        logger.error('an exception occurred', exc_info=True)