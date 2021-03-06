import csv
import os.path
import pandas as pd
from logging_module import *
import user_account
from datetime import datetime, time


class Messenger:

    def __init__(self, username, username2=None, message=None):
        self.username = username
        self.username2 = username2
        self.message = message
        self.is_read = False  # A Boolean for checking the read or unread a message

    def saving_info_in_file(self, file_name, username):

        date_time = Messenger.date_time()
        data = [self.message, date_time, self.is_read, self.username, self.username2]
        headers = ['message', 'date-time', 'is_send', 'Sender', 'Receiver']
        list_data = [data]
        df_data = pd.DataFrame(list_data, columns=headers)
        with open(f'users\\{username}\\{file_name}', mode='a') as file:
            df_data.to_csv(file, mode='a', index=False, header=False)

        return df_data

    @staticmethod
    def loading_data_from_csvfile_to_dataframe(file_name, username):
        if os.path.exists(f'users\\{username}\\{file_name}'):
            with open(f'users\\{username}\\{file_name}', mode='r') as file:
                reader = csv.DictReader(file)
                df = pd.DataFrame(reader)
            return df
        else:
            with open(f'users\\{username}\\{file_name}', 'a') as file:
                headers = ['message', 'date-time', 'is_send', 'Sender', 'Receiver']
                writer = csv.DictWriter(file, fieldnames=headers)
                if file.tell() == 0:
                    writer.writeheader()
            return writer

    def number_of_all_messages(self, csvfile_name):
        unread_messages = Messenger.unread_messages(self, csvfile_name)
        logger.warning(f'the number of unread messages for user :{self.username} is {unread_messages}')
        df = Messenger.loading_data_from_csvfile_to_dataframe(csvfile_name, self.username)
        number_of_rows = len(df.index)
        return number_of_rows

    def unread_messages(self, csvfile_name):
        # Get a bool series representing which row
        # satisfies the condition i.e. True for
        # row in which 'is_read' is 'False'
        df = Messenger.loading_data_from_csvfile_to_dataframe(csvfile_name, self.username)
        df = df.apply(lambda x: True if x['is_read'] == "False" else False, axis=1)
        # Count number of False in the series
        num_rows = len(df[df == True].index)
        return num_rows

    def read_message(self, index, csvfile_name):
        # first get all messages in cdv file
        df = Messenger.loading_data_from_csvfile_to_dataframe(file_name=csvfile_name,
                                                              username=self.username)
        # according to index that user entered,shows that message
        message_output = df.at[index, 'message']
        # the message after reading should get tag read
        self.is_read = True
        # updating dataframe and csv file
        Messenger.update_column_value_of_dataframe(self, csvfile_name, index, 'is_read', 'True')
        return message_output

    def delete_message(self, csvfile_name, index):
        # for delete one message from draft if send it
        # with pandas
        df = Messenger.loading_data_from_csvfile_to_dataframe(csvfile_name, self.username)
        df.drop(index=df.index[index],
                axis=0,
                inplace=True)
        # updating csv file
        df.to_csv(f'users\\{self.username}\\{csvfile_name}', index=False)
        return 'one message was deleted'

    def update_column_value_of_dataframe(self, file_name, index, column_name, new_value):

        df = pd.read_csv(f'users\\{self.username}\\{file_name}')
        # updating the column value/data
        df.loc[index, column_name] = new_value
        # writing into the file
        df.to_csv(f'users\\{self.username}\\{file_name}', index=False)
        return df

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
        # for writing in csv file and dataframe
        now = datetime.now()
        now_time = time(now.hour, now.minute, now.second)
        now_date = now.date()
        date_time = datetime.combine(now_date, now_time)
        str_date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
        return str_date_time

    def sending_message(self):
        # send message from username1 to username2
        my_tuple = user_account.User.get_info_from_csvfile()
        username_list = my_tuple[1]
        validation = False
        if self.username2 in username_list:

            if Messenger.wanting_to_sent_message():
                validation = True
                Messenger.saving_info_in_file(self, file_name='sent.csv', username=self.username)
                Messenger.saving_info_in_file(self, file_name='inbox.csv', username=self.username2)
                logger.info(f'the user : {self.username} send a message to {self.username2}')
                print(f'you send a message to {self.username2}')
            else:
                Messenger.saving_info_in_file(self, file_name='draft.csv', username=self.username)
                print(f'message saved in draft')
        else:
            logger.warning('this username not exist!!!')
        return validation
