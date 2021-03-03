from conftest import ROOT_DIR
from src.utils_package.utils_module import read_file

configuration = read_file(ROOT_DIR + "//configuration.json")
input_data = read_file(ROOT_DIR + configuration["inputData"])
json_users = read_file(ROOT_DIR + configuration["dataJson"])
docs_files_folder = ROOT_DIR + '//src//resources//other_files//docs_types'
pdf_folder_files = ROOT_DIR + '//src//resources//other_files//pdf_types'
log_files = ROOT_DIR + "//src//docs//logs//"


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

    TXT_FILE = docs_files_folder + "test.txt"

    # PDF NAMES
    pdf_file_name = "Some_pdf.pdf"
    pdf_file = pdf_folder_files + pdf_file_name