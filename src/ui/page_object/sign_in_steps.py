import allure

from src.resources.input_data.data_and_params import DataUI
from src.ui.page_object.pages.sign_in_page import SignInPage


class SignInSteps(SignInPage):

    @allure.step("Fill all required fields for sign in")
    def fill_required_fields_for_login(self, user):
        self.at_page()
        self.email_field_input_value(DataUI().email(user))
        self.password_field_input_value(DataUI().password(user))
        self.submitlogin_button_click()