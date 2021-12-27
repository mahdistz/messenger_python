from user_account import *
from logging_module import *
from working_in_messenger import *


# for using in menu . calling for check to register
def checking_for_register(username, password):
    validation = False
    an_user = Register(username, password)

    if an_user.validation_username():
        print(f'this username {username} is correct')
        if an_user.validation_password():
            again_password = input('repeat password : ')
            if password == again_password:
                print('you successfully added to Messenger.')
                validation = True
            else:
                logger.error('The password you entered does not match the default password.try again')
        else:
            print('the password is not correct!')
    else:
        logger.info('this username is not correct! please try again...')

    return validation


# to calling in menu (in options 1(Register) and 2(Login) in menu )
def getting_into_messenger(user):
    while True:
        try:
            input1 = input('1)Inbox\n2)Draft\n3)Sent\n4)Create New Message\n5)Log Out\n>>>')
            if input1 == '1':
                menu_into_files()
                input2 = input('>>>')

                if input2 == '1':
                    Messenger.number_of_all_messages(user, 'inbox.csv')
                    all_messages = Messenger.loading_data_from_csvfile_to_dataframe('inbox.csv', user.username)
                    print(all_messages)

                elif input2 == '2':
                    all_messages = Messenger.loading_data_from_csvfile_to_dataframe('inbox.csv', user.username)
                    print(all_messages)

                    item = int(input('Enter index of messages to read this!\n>>>'))
                    numbers = Messenger.number_of_all_messages(user, 'inbox.csv')

                    if item in range(numbers):
                        print(Messenger(user.username).read_message(index=int(item), csvfile_name='inbox.csv'))
                    else:
                        logger.error('index error!there is no message with this index', exc_info=True)

                    input3 = input('1)reply\n2)delete\n3)forward\n>>>')

                    if input3 == '1':
                        message = input('Enter your message\n>>> ')
                        df = Messenger.loading_data_from_csvfile_to_dataframe('inbox.csv', user.username)
                        sender = df.at[int(item), 'Sender']
                        Inbox(message=message, username1=user.username, username2=sender).reply_to_one_message()

                    elif input3 == '2':
                        Messenger(user).delete_message(index=int(item), csvfile_name='inbox.csv')

                    elif input3 == '3':
                        print(users_list)
                        user2 = input('Enter username of whom you want forward message\n>>>')
                        if user2 in users_list:
                            df = Messenger.loading_data_from_csvfile_to_dataframe('inbox.csv', user.username)
                            message = df.at[int(item), 'message']
                            Inbox(message=message, username1=user.username, username2=user2).forward_message()
                        else:
                            logger.error('this username not exist!')
                    else:
                        raise ValueError('you should enter 1 or 2 or 3')

            elif input1 == '2':

                menu_into_files()
                input2 = input('>>>')

                if input2 == '1':
                    all_messages = Messenger.loading_data_from_csvfile_to_dataframe('draft.csv', user.username)
                    print(all_messages)

                elif input2 == '2':

                    all_messages = Messenger.loading_data_from_csvfile_to_dataframe('draft.csv', user.username)
                    print(all_messages)
                    item = int(input('Enter index of messages to read this!\n>>>'))
                    numbers = Messenger.number_of_all_messages(user, 'draft.csv')
                    if item in range(numbers):
                        print(Messenger(user.username).read_message(index=int(item), csvfile_name='draft.csv'))
                    else:
                        logger.error('index error!there is no message with this index', exc_info=True)

                    input3 = input('1)delete\nr2)sending message\n>>>')

                    if input3 == '1':
                        Messenger(user).delete_message(index=int(item), csvfile_name='draft.csv')

                    elif input3 == '2':
                        print(users_list)
                        user2 = input('Enter username of whom you want forward message:')
                        if user2 in users_list:
                            df = Messenger.loading_data_from_csvfile_to_dataframe('draft.csv', user.username)
                            message = df.at[item, 'message']
                            Draft(message=message, username1=user.username, username2=user2). \
                                sent_one_message_from_draft(item)
                        else:
                            logger.error('this username not exist')
                    else:
                        raise ValueError('you should enter 1 or 2')

            elif input1 == '3':
                menu_into_files()
                input2 = input('>>>')

                if input2 == '1':
                    all_messages = Messenger.loading_data_from_csvfile_to_dataframe('sent.csv', user.username)
                    print(all_messages)

                elif input2 == '2':
                    print(Messenger.loading_data_from_csvfile_to_dataframe('sent.csv', user.username))

                    item = int(input('Enter index of messages to read this!\n>>>'))
                    numbers = Messenger.number_of_all_messages(user, 'sent.csv')
                    if item in range(numbers):
                        print(Messenger(user.username).read_message(index=int(item), csvfile_name='sent.csv'))
                    else:
                        logger.error('index error!there is no message with this index', exc_info=True)

                    input3 = input('1)delete\r2)forward\r>>>')

                    if input3 == '1':
                        Messenger(user).delete_message(index=int(item), csvfile_name='sent.csv')

                    elif input3 == '2':
                        print(users_list)
                        user2 = input('Enter username of whom you want forward message\n>>>')
                        if user2 in users_list:
                            df = Messenger.loading_data_from_csvfile_to_dataframe('sent.csv', user.username)
                            message = df.at[int(item), 'message']
                            Sent(message=message, username1=user.username, username2=user2).forward_a_message()
                        else:
                            logger.error('this username not exist!')
                    else:
                        raise ValueError('you should enter 1 or 2 or 3')

            elif input1 == '4':

                print(users_list)
                user2 = input('Enter username of whom you want to send message\n>>>')
                if user2 in users_list:
                    message = input('Enter your message:')
                    Messenger(username=user.username, username2=user2, message=message).sending_message()
                else:
                    logger.error('this username not exist!')

            elif input1 == '5':
                User.quit_from_messenger(user.username)
                break
            else:
                raise ValueError('you should enter a number between 1 to 5!!')

        except (ValueError, TypeError):
            logger.error('an exception occurred', exc_info=True)

        except (NameError, IOError, FileNotFoundError):
            logger.error('an exception occurred', exc_info=True)

        except (FileExistsError, ModuleNotFoundError) :
            logger.error('an exception occurred', exc_info=True)

        except Exception :
            logger.error('an exception occurred', exc_info=True)


def menu_into_files():
    # files : draft , sent , inbox
    print('\n1)Show all messages\n2)read messages')


my_tuple = User.get_info_from_csvfile()
users_list = my_tuple[1]

"""
Menu
"""

while True:
    try:
        my_input = input('"""Welcome to Messenger"""\n1)Register\n2)Login\n3)Exit\n>>> ')

        if my_input == '1':
            # Register
            # condition for correct username and password
            print('username must be 3 to 12 characters and can include letters,numbers and "-" ,"." ,"_" ')
            print("Password must be 6 to 12 characters,1 lowercase letter,1 uppercase letter,1 digit")
            # get input from user
            username_input1 = input('Enter username: ')
            password_input1 = input('Enter password: ')
            # checking username and password that user entered
            if username_input1 not in users_list:
                validation_register = checking_for_register(username_input1, password_input1)
                # validation_register >> A Boolean : True / False
                if validation_register:

                    user = Register(username_input1, password_input1).register()
                    # user registered successfully!
                    # create folder and csv files for user
                    user.creating_folder_for_each_user()
                    user.creating_csvfile_for_each_user()
                    print(' you have registered successfully :) ')
                    getting_into_messenger(user)
                else:
                    logger.info('validation is false .please try again...')
            else:
                logger.warning("this username is not available.try Again...")

        elif my_input == '2':
            # Login
            username_input = input('Enter username: ')
            password_input = input('Enter password: ')
            login_user = Login(username_input, password_input)
            if not login_user.locking:
                if login_user.login():
                    print('you have successfully entered the program :) ')
                    # user login to messenger successfully!
                    getting_into_messenger(login_user)
            else:
                logger.warning(f'this account is locked for 1 hour.because user entered '
                               f'incorrect password for 3 time.')

        elif my_input == '3':

            input4 = input('Are you Sure to Exit from Messenger?(yes/no)\n>>>')

            if input4 == 'yes':
                break
            elif input4 == 'no':
                continue
            else:
                raise ValueError('you should enter yes or no')
        else:
            raise ValueError('you should enter 1 or 2 or 3')

    except (ValueError, TypeError) as error:
        logger.error('an exception occurred', exc_info=True)

    except (NameError, IOError, FileNotFoundError) as error:
        logger.error('an exception occurred', exc_info=True)

    except (FileExistsError, ModuleNotFoundError) as error:
        logger.error('an exception occurred', exc_info=True)

    except Exception as e:
        logger.error('an exception occurred', exc_info=True)
