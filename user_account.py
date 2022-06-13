from working_in_messenger import *
import os
from hashlib import sha3_256
from re import compile
from file_handling import *
from datetime import datetime, timedelta

PASSWORD_REGEX = compile(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,12}\Z')
USERNAME_REGEX = compile(r'\A[\w\-\.]{3,12}\Z')


# parent af Register and Login classes
class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def hash_method(obj):
        obj_hashing = sha3_256(obj.encode('ascii')).hexdigest()
        return obj_hashing

    @staticmethod
    def get_info_from_csvfile():
        """
        This method reads the csv file (or create this) and return a tuple.
        information_list -->> a list of dictionaries of 'username and password(hashing)' of each user
        users_list -->> list of usernames
        passwords_list -->> list of passwords(hashing)
        locking_list -->> list of self.Lock
        :return: ([{'username':...,'password(hash)':...}],[usernames],[passwords],[locking])
        """
        # usernames list
        users_list = []
        # password list
        passwords_list = []
        # locking list
        locking_list = []
        my_file = File('users_information.csv')
        if os.path.exists('users_information.csv'):
            information_list = my_file.read_csvfile_as_dictionary()
            for item in information_list:
                users_list.append(item['username'])
                passwords_list.append(item['password'])
                locking_list.append(item['locking'])
        else:
            # creating csv file
            my_file.write({'username': '', 'password': '', 'locking': ''})
            information_list = []
        return information_list, users_list, passwords_list, locking_list

    def quit_from_messenger(self):
        logger.info(f'{self.username} log out from messenger')
        print(f'{self.username} log out from messenger')


class Register(User):
    def __init__(self, username, password):
        super(Register, self).__init__(username, password)
        self.locking = False

    def validation_password(self):
        # Password must be 6 to 12 characters, 1 lowercase letter
        # 1 uppercase letter,1 digit
        return PASSWORD_REGEX.match(self.password) is not None

    def validation_username(self):
        # username must be 3 to 12 characters and can include
        # letters,numbers and "-" ,"." ,"_"
        return USERNAME_REGEX.match(self.username) is not None

    def creating_folder_for_each_user(self):
        """
        this method first create users folder then,
        Creates a folder for each user called the username of that user
        """
        if not os.path.exists(f'users\\{self.username}'):
            os.makedirs(f'users\\{self.username}')

    def creating_csvfile_for_each_user(self):
        """
        in each folder of usernames creates 3 csv file for
        handling sent ,draft and inbox
        """
        items = ['sent.csv', 'draft.csv', 'inbox.csv']
        for item in items:
            with open(f'users\\{self.username}\\{item}', 'a') as file:
                headers = ['message', 'date-time', 'is_read', 'Sender', 'Receiver']
                writer = csv.DictWriter(file, fieldnames=headers)
                if file.tell() == 0:
                    writer.writeheader()

    def writing_in_file(self):
        # for each user ,username and password must be saved in file
        info = {'username': self.username, 'password': User.hash_method(self.password), 'locking': self.locking}
        File('users_information.csv').write(info)

    def register(self):

        my_tuple = User.get_info_from_csvfile()
        usernames_list = my_tuple[1]

        if self.username not in usernames_list:
            Register.writing_in_file(self)
            logger.info(f" new person with username: {self.username},registered into program")
            return True
        else:
            # This means there is a user with this username and this username is not available
            logger.warning(f"this username: {self.username} is not available.try Again...")
            return False


class Login(User):

    def __init__(self, username, password):
        super(Login, self).__init__(username, password)
        self.locking = False

    def locking_account(self):
        # if a user enter incorrect password for 3 time then his/her account
        # locked for one hour
        self.locking = True
        df = pd.read_csv('users_information.csv')
        index_list = df.index[(df['username'] == self.username)].tolist()
        index = int(index_list[0])
        # update dataframe
        df.loc[index, 'locking'] = 'True'
        # writing into the file
        df.to_csv('users_information.csv', index=False)
        now = datetime.now()
        unlocking_account = now + timedelta(hours=1)
        return unlocking_account

    def unlock_account(self):

        un_lock_time = Login.locking_account(self)
        now = datetime.now()
        if un_lock_time >= now:
            self.locking = False
            df = pd.read_csv('users_information.csv')
            index_list = df.index[(df['username'] == self.username)].tolist()
            index = int(index_list[0])
            # update dataframe
            df.loc[index, 'locking'] = 'False'
            # writing into the file
            df.to_csv('users_information.csv', index=False)

    def login(self):

        my_tuple = User.get_info_from_csvfile()
        users_list = my_tuple[1]
        password_list = my_tuple[2]
        lock_list = my_tuple[3]
        if self.username not in users_list:
            logger.error(f'this username:{self.username} not exist!')
            return False
        else:
            for i in range(len(users_list)):
                if users_list[i] == self.username:
                    if password_list[i] == User.hash_method(self.password):
                        if lock_list[i] == 'False':
                            logger.info(f'"{self.username}" have successfully entered the program ')
                            return True
                        else:
                            Login.unlock_account(self)
                            logger.warning('your account is locked')
                    else:
                        print('the password is not correct.you can try 2 more times.')
                        if Login.incorrect_password(self) and lock_list[i] == 'False':
                            logger.info(f'"{self.username}" have successfully entered the program ')
                            return True
                        else:
                            # if user can't enter true password her/his account must be locked.
                            Login.locking_account(self)
                            logger.warning(f'this account :"{self.username}" is locked for 1 hour.because user'
                                           f' entered incorrect password for 3 time.')
                            return False

    def incorrect_password(self):
        """
        The user is allowed to enter his password 3 times in total.
        in login method he/she enters the wrong password once and in this method he/she can try 2 more times.
        :return: 'correct_password' is True when user enters true password
        """
        # find true password by reading csv_file
        info_list = User.get_info_from_csvfile()
        for item in info_list[0]:
            # info_list[0] -->> [{'username','password(hash)'}]
            if item['username'] == self.username:
                true_password = item['password']
        correct_password = False
        count = 0
        while count < 2:
            repeat_password = input('Repeat Your Password: ')
            count += 1
            # 'password' is hashed.So 'repeat_pass' must also be hashed,that they can be compared.
            if User.hash_method(repeat_password) == true_password:
                correct_password = True
                break
        return correct_password
