import allure

from src.ui.page_object.pages.user_bar_page import UserBarPage


class UserBarSteps(UserBarPage):

    @allure.step("Login to account")
    def login_to_account(self):
        self.sign_in_button_click()
        return self