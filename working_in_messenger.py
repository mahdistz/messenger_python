import pandas as pd
from logging_module import *
from user_account import *
from datetime import datetime, time
import os
import re


class Messenger:
    counter = 1
    data_list = []
    instance_list = []

    def __init__(self, message, username1, username2):
        self.username1 = username1
        self.username2 = username2
        self.message = message
        self.number = Messenger.counter
        Messenger.counter += 1
        self.is_read = False  # A Boolean for checking the read or unread a message
        self.is_send = False  # A Boolean for checking the message is sending or not
        Messenger.instance_list.append(self)

    def saving_info_in_file(self, file_name, username):

        date_time = Messenger.date_time()
        message_path = f'users\\{username}\\{file_name}\\message-{self.number}'
        data = [self.number, message_path, date_time, self.is_read, self.is_send, self.username1, self.username2]
        headers = ['message_number', 'message_path', 'date-time', 'is_read', 'is_send', 'Sender', 'Receiver']
        Messenger.data_list.append(data)
        df_data = pd.DataFrame(Messenger.data_list, columns=headers)
        df_data.to_csv(f'users\\{username}\\{file_name}\\information.csv')

        return df_data

    def save_message_into_folder(self, file_name, username):

        lines = Messenger.get_all_sentence_in_string(self.message)
        lines1 = [item + '\n' for item in lines]
        with open(os.path.join(f'users\\{username}\\{file_name}', f'message-{self.number}' + ".txt"), 'w+') as file:
            file.writelines(lines1)

        return lines1

    def number_of_all_messages(self, file_name):
        unread_messages = []

        list_1 = os.listdir(f'users\\{self.username1}\\{file_name}')
        logger.warning(f'the number of unread messages for user :{self.username1} is {len(unread_messages)}')
        return len(list_1)-1

    def read_message(self):
        # in this method one message after reading should get tag read
        self.is_read = True
        return self.is_read

    def delete_message(self, folder_name):
        os.remove(f'users\\{self.username1}\\{folder_name}\\{self.message}')

    @staticmethod
    def wanting_to_sent_message():
        try:
            wanting = input('Are You Sure To Send This Message??(yes/no):').lower()
            if wanting == 'yes':
                return True
            elif wanting == 'no':
                return False
            else:
                raise ValueError('You should enter "yes" or "no" !!')
        except (ValueError, TypeError) as e:
            print(e)

    @staticmethod
    def date_time():
        now = datetime.now()
        now_time = time(now.hour, now.minute, now.second)
        now_date = now.date()
        date_time = datetime.combine(now_date, now_time)
        str_date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
        return str_date_time

    @staticmethod
    def get_all_sentence_in_string(string):
        # pattern : to find all sentence in a string or words
        pattern = re.compile(r'([\w][^\.!?]*[\.!?]*|[\w][^\.!?]*)', re.M)
        sentence_list = pattern.findall(string)
        return sentence_list


class Inbox(Messenger):
    counter = 1

    def __init__(self, message, username1, username2):
        super().__init__(message, username1, username2)
        self.number = Inbox.counter
        Inbox.counter += 1

    def read_message(self):
        pass

    def number_of_all_messages(self, file_name):
        super(Inbox, self).number_of_all_messages(self)

    def reply_to_one_message(self):
        logger.info(f'the user : {self.username1} reply a message in Inbox folder')
        return f"in this method user:{self.username1} can reply to one of the messages in inbox folder"

    def number_of_unread_messages(self):
        # number of unread message = number of total message - number of read messages
        logger.warning(f'the numer of unread messages for user {self.username1} is : ...')
        return "this method returned number of unread messages"

    def get_tag_read(self):
        # The read messages gets the tag read
        self.is_read = True
        return "the read messages get the tag 'read'"


class Draft(Messenger):
    counter = 1

    def __init__(self, message, username1, username2):
        super().__init__(message, username1, username2)
        self.number = Draft.counter
        Draft.counter += 1

    def read_message(self):
        super(Draft, self).read_message()

    def number_of_all_messages(self, file_name='Draft'):
        super(Draft, self).number_of_all_messages()

    def sent_one_message_from_draft(self):
        self.is_send = True
        logger.info(f'the user:{self.username1} sent of message from draft folder')
        return f"in this method user:{self.username1} can be sent one of the messages in draft folder."

    def get_tag_sent(self):
        # if one message of draft has sent it gets the tag sent
        # and move to inbox of user who sent message to her/him
        self.is_send = True
        return "the sent message should get tag sent"


class Sent(Messenger):
    counter = 1

    def __init__(self, message, username1, username2):
        super().__init__(message, username1, username2)
        self.number = Sent.counter
        Sent.counter += 1

    def number_of_all_messages(self, file_name='Sent'):
        super().number_of_all_messages(self)

    def read_message(self):
        super(Sent, self).read_message()

    def forward_a_message(self):
        # get username of whom you want to sent message
        # get message's text for sending
        self.is_send = True
        logger.info(f'user:{self.username1} sent a message to user: {self.username2}')


class NewMessage(Messenger):
    counter = 1

    def __init__(self, message, username1, username2):
        super().__init__(message, username1, username2)
        self.number = NewMessage.counter
        NewMessage.counter += 1

    def sending_message(self, username2):
        # send message from username1 to username2
        my_tuple = User.get_info_from_csvfile()
        username_list = my_tuple[1]
        if username2 in username_list:
            if Messenger.wanting_to_sent_message():
                pass
            else:
                pass
        else:
            logger.warning('this username not exist!!!')
