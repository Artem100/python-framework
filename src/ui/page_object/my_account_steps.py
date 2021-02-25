import allure

from src.ui.page_object.pages.my_account_page import MyAccountPage


class MyAccountSteps(MyAccountPage):

    @allure.step("User in *Profile account* after login")
    def user_in_account_after_login(self):
        self.at_page()
        self.return_home_button_display()