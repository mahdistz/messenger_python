import logging
import file_handling
import os


class Messenger:

    def __init__(self):
        self.messenger = 'messenger'

    def number_of_all_messages(self):
        pass

    def read_message(self):
        pass


class Inbox(Messenger):

    def read_message(self):
        super(Inbox, self).read_message()

    def reply_to_one_message(self):
        pass

    def number_of_unread_messages(self):
        pass

    def number_of_all_messages(self):
        super(Inbox, self).number_of_all_messages()

    def get_tag_read(self):
        # The read message gets the tag read
        pass


class Draft(Messenger):

    def read_message(self):
        super(Draft, self).read_message()

    def number_of_all_messages(self):
        super(Draft, self).number_of_all_messages()

    def sent_one_message_draft(self):
        pass

    def get_tag_sent(self):
        # if one message of draft has sent it gets the tag sent
        # and move to inbox of user who sent message to her/him
        pass


class Sent(Messenger):

    def number_of_all_messages(self):
        super().number_of_all_messages()

    def read_message(self):
        super(Sent, self).read_message()

    def sent_a_message(self):
        # get username of whom you want to sent message
        pass
