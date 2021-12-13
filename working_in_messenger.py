import logging
import file_handler_module
import os


class Messenger:
    def __init__(self):
        self.messenger = 'messenger'


class Inbox(Messenger):
    pass


class Draft(Messenger):
    pass


class Sent(Messenger):
    pass

