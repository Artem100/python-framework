import allure
import pytest

from src.resources.input_data.data_and_params import DataUI
from src.ui.page_object.main_steps import MainSteps
from src.ui.page_object.my_account_steps import MyAccountSteps
from src.ui.page_object.sign_in_steps import SignInSteps
from src.ui.page_object.user_bar_steps import UserBarSteps

pytestmark = [pytest.mark.ui, pytest.mark.Login]

data_ui = DataUI()

class TestLogin():

    @pytest.fixture(autouse=True)
    def setup(self, get_driver):
        self.driver = get_driver
        self.sign_in = SignInSteps(self.driver)
        self.my_account_page = MyAccountSteps(self.driver)
        self.user_bar = UserBarSteps(self.driver)
        self.main_page = MainSteps(self.driver)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("Sign in")
    @allure.title("Test 1 - Positive Sing in")
    def test_01(self):
        self.main_page.open_main_page_url()
        self.user_bar.sign_in_button_click()
        self.sign_in.fill_required_fields_for_login(data_ui.USER_DATA)
        self.my_account_page.user_in_account_after_login()