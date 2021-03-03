import allure
from selenium.webdriver.common.by import By

from src.ui.page_object.pages.base_page import BasePage


class ContactUsPage(BasePage):

    TITLE_PAGE = "Contact us - My Store"

    SUBJECT_HEADING_LIST_BUTTON = (By.CSS_SELECTOR, "select#id_contact", "SUBJECT HEADING LIST BUTTON")
    EMAIL_FIELD = (By.CSS_SELECTOR, "input#email", "EMAIL FIELD")
    ATTACH_FILE_FIELD = (By.CSS_SELECTOR, "input#fileUpload", "ATTACH FILE FIELD")
    MESSAGE_FIELD = (By.CSS_SELECTOR, "textarea#message", "MESSAGE FIELD")
    SEND_BUTTON = (By.CSS_SELECTOR, "button#submitMessage", "SEND BUTTON")

    def at_page(self):
        self.title_page(self.TITLE_PAGE)
        return self

    @allure.step("Subject heading list button click")
    def subject_heading_list_button_click(self):
        self.click(*self.SUBJECT_HEADING_LIST_BUTTON)
        return self

    @allure.step("In *Subject heading list* select 'Customer service' value")
    def in_subject_heading_list_select_customer_service(self):
        text = 'Customer service'
        self.select_value_in_dropdown_by_option_visible_text(text, *self.SUBJECT_HEADING_LIST_BUTTON)

    @allure.step("Input value to *Email* field")
    def email_field_input(self, value):
        self.backspace_button_all(*self.EMAIL_FIELD)
        self.enter_text(value, *self.EMAIL_FIELD)
        return self

    @allure.step("Upload attached file")
    def attach_file_upload(self, path):
        self.upload_file(path, *self.ATTACH_FILE_FIELD)
        return self

    @allure.step("Filling message field")
    def message_field_input(self, text):
        self.enter_text(text, *self.MESSAGE_FIELD)
        return self

    @allure.step("*Send* button click")
    def send_button_click(self):
        self.click(*self.SEND_BUTTON)
        return self