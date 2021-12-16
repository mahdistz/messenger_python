import logging
import user_account
import file_handling
import os

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


class Messenger(user_account.User):

    def __init__(self, username, password):
        super().__init__(username, password)

        self.messenger = 'messenger'
        self.number = 'number_of_all_messages'
        self.reading = False  # A Boolean for checking the read or unread a message
        self.sending = False  # A Boolean for checking the message is sending or not

    def number_of_all_messages(self):
        logger.warning(f'the number of unread messages for user :{self.username} is {self.number}')
        return "this method returned the number of all messages "

    def read_message(self):
        # in this method one message after reading should get tag read
        self.reading = True
        logger.info('one message was read')
        return "this method read a message and show this to user"


class Inbox(Messenger):

    def read_message(self):
        super(Inbox, self).read_message()

    def number_of_all_messages(self):
        super(Inbox, self).number_of_all_messages()

    def reply_to_one_message(self):
        logger.info(f'the user : {self.username} reply a message in Inbox folder')
        return f"in this method user:{self.username} can reply to one of the messages in inbox folder"

    def number_of_unread_messages(self):
        # number of unread message = number of total message - number of read messages
        logger.warning(f'the numer of unread messages for user {self.username} is : ...')
        return "this method returned number of unread messages"

    def get_tag_read(self):
        # The read messages gets the tag read
        self.reading = True
        return "the read messages get the tag 'read'"


class Draft(Messenger):

    def read_message(self):
        super(Draft, self).read_message()

    def number_of_all_messages(self):
        super(Draft, self).number_of_all_messages()

    def sent_one_message_from_draft(self):
        self.sending = True
        logger.info(f'the user:{self.username} sent of message from draft folder')
        return f"in this method user:{self.username} can be sent one of the messages in draft folder."

    def get_tag_sent(self):
        # if one message of draft has sent it gets the tag sent
        # and move to inbox of user who sent message to her/him
        self.sending = True
        return "the sent message should get tag sent"


class Sent(Messenger):

    def number_of_all_messages(self):
        super().number_of_all_messages()

    def read_message(self):
        super(Sent, self).read_message()

    def sent_a_message(self, other, text_of_message):
        # get username of whom you want to sent message
        # get message's text for sending
        self.sending = True
        logger.warning(f'user:{self.username} sent a message to user: {other.username}')
        return f"in this method user: {self.username} can be sent a message to other user"
