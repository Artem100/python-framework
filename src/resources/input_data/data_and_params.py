from conftest import ROOT_DIR
from src.utils_package.utils_module import read_file

configuration = read_file(ROOT_DIR + "//configuration.json")
input_data = read_file(ROOT_DIR + configuration["inputData"])
json_users = read_file(ROOT_DIR + configuration["dataJson"])

class DataUI:

    MAIN_PAGE_UI_URL = json_users['ui']

    @staticmethod
    def email(user):
        login = json_users['creds'][user]['email']
        return login

    @staticmethod
    def password(user):
        password = json_users['creds'][user]['password']
        return password

    USER_DATA = input_data['user']
    USER_EMAIL = input_data['email_user']