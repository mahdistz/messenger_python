import pandas as pd
from logging_module import *
from user_account import *
from datetime import datetime, time


class Messenger:

    def __init__(self, username1, username2='', message=''):
        self.username1 = username1
        self.username2 = username2
        self.message = message
        self.is_read = False  # A Boolean for checking the read or unread a message

    def saving_info_in_file(self, file_name, username):

        date_time = Messenger.date_time()
        data = [self.message, date_time, self.is_read, self.username1, self.username2]
        headers = ['message', 'date-time', 'is_send', 'Sender', 'Receiver']
        list_data = [data]
        df_data = pd.DataFrame(list_data, columns=headers)
        with open(f'users\\{username}\\{file_name}', mode='a+') as file:
            df_data.to_csv(file, mode='a', index=False, header=False)

        return df_data

    @staticmethod
    def loading_data_from_csvfile_to_dataframe(file_name, username):
        with open(f'users\\{username}\\{file_name}', mode='r') as file:
            reader = csv.DictReader(file)
            df = pd.DataFrame(reader)
        return df

    def number_of_all_messages(self, csvfile_name):
        unread_messages = Messenger.unread_messages(self, csvfile_name)
        df = Messenger.loading_data_from_csvfile_to_dataframe(csvfile_name, self.username1)
        number_of_rows = len(df.index)
        logger.warning(f'the number of unread messages for user :{self.username1} is {unread_messages}')
        return number_of_rows

    def unread_messages(self, csvfile_name):
        # Get a bool series representing which row
        # satisfies the condition i.e. True for
        # row in which 'is_read' is 'False'
        df = Messenger.loading_data_from_csvfile_to_dataframe(csvfile_name, self.username1)
        df = df.apply(lambda x: True if x['is_read'] == "False" else False, axis=1)
        # Count number of False in the series
        num_rows = len(df[df == True].index)
        return num_rows

    def read_message(self, index, csvfile_name):
        # first get all messages in cdv file
        df = Messenger.loading_data_from_csvfile_to_dataframe(csvfile_name, self.username1)
        # according to index that user entered,shows that message
        message_output = df.at[index, 'message']
        # the message after reading should get tag read
        self.is_read = True
        # updating dataframe and csv file
        Messenger.update_column_value_of_dataframe(self, csvfile_name, index, 'is_read', 'True')
        return message_output

    def delete_message(self, csvfile_name, index):
        # with pandas
        df = Messenger.loading_data_from_csvfile_to_dataframe(csvfile_name, self.username1)
        df.drop(index=df.index[index],
                axis=0,
                inplace=True)
        # updating csv file
        df.to_csv(f'users\\{self.username1}\\{csvfile_name}', index=False)
        return df

    def update_column_value_of_dataframe(self, file_name, index, column_name, new_value):

        df = pd.read_csv(f'users\\{self.username1}\\{file_name}')
        # updating the column value/data
        df.loc[index, column_name] = new_value
        # writing into the file
        df.to_csv(f'users\\{self.username1}\\{file_name}', index=False)
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
        my_tuple = User.get_info_from_csvfile()
        username_list = my_tuple[1]
        validation = False
        if self.username2 in username_list:

            if Messenger.wanting_to_sent_message():
                validation = True
                Messenger.saving_info_in_file(self, file_name='sent.csv', username=self.username1)
                Messenger.saving_info_in_file(self, file_name='inbox.csv', username=self.username2)
            else:
                Messenger.saving_info_in_file(self, file_name='draft.csv', username=self.username1)
        else:
            logger.warning('this username not exist!!!')
        return validation

    def quit_from_messenger(self):
        logger.info(f'{self.username1} log out from message')


class Inbox(Messenger):

    def __init__(self, message, username1, username2):
        super().__init__(message, username1, username2)

    def read_message(self, index, csvfile_name='inbox.csv'):
        output = super(Inbox, self).read_message(index, csvfile_name='inbox.csv')
        return output

    def number_of_all_messages(self, csvfile_name='inbox.csv'):
        output = super(Inbox, self).number_of_all_messages(csvfile_name='inbox.csv')
        return output

    def reply_to_one_message(self):
        if Messenger.sending_message(self):
            logger.info(f'the user : {self.username1} reply a message from Inbox')

    def unread_messages(self, csvfile_name='inbox.csv'):
        output = super(Inbox, self).unread_messages(csvfile_name='inbox.csv')
        return output

    def forward_message(self):
        if Messenger.sending_message(self):
            logger.info(f'the user : {self.username1} forward a message from Inbox to {self.username2}')


class Draft(Messenger):

    def __init__(self, message, username1, username2='Null'):
        super().__init__(message, username1, username2)

    def read_message(self, index, csvfile_name='draft.csv'):
        output = super(Draft, self).read_message(index, csvfile_name='draft.csv')
        return output

    def number_of_all_messages(self, csvfile_name='draft.csv'):
        output = super(Draft, self).number_of_all_messages(csvfile_name='draft.csv')
        return output

    def sent_one_message_from_draft(self, index):
        # send message from username1 to username2
        my_tuple = User.get_info_from_csvfile()
        username_list = my_tuple[1]

        if self.username2 in username_list:

            if Messenger.wanting_to_sent_message():

                Messenger.saving_info_in_file(self, file_name='sent.csv', username=self.username1)
                Messenger.saving_info_in_file(self, file_name='inbox.csv', username=self.username2)
                logger.info(f'the user:{self.username1} sent a message from draft to {self.username2}')
                Messenger.delete_message(self.username1, 'draft.csv', index=index)
            else:
                pass
        else:
            logger.warning('this username not exist!!!')


class Sent(Messenger):

    def __init__(self, message, username1, username2):
        super().__init__(message, username1, username2)

    def read_message(self, index, csvfile_name='sent.csv'):
        output = super(Sent, self).read_message(index, csvfile_name='sent.csv')
        return output

    def number_of_all_messages(self, csvfile_name='sent.csv'):
        output = super(Sent, self).number_of_all_messages(csvfile_name='sent.csv')
        return output

    def forward_a_message(self):
        if Messenger.sending_message(self.username1):
            logger.info(f'user:{self.username1} sent a message to user: {self.username2}')
