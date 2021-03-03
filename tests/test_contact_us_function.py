import allure
import pytest

from src.resources.input_data.data_and_params import DataUI
from src.resources.input_data.title_messages import TitleMessages
from src.ui.page_object.contact_us_steps import ContactUsSteps
from src.ui.page_object.main_steps import MainSteps
from src.ui.page_object.my_account_steps import MyAccountSteps
from src.ui.page_object.pages.filter_page import FilterPage
from src.ui.page_object.sign_in_steps import SignInSteps
from src.ui.page_object.user_bar_steps import UserBarSteps

pytestmark = [pytest.mark.ui, pytest.mark.Contact]

class TestContract():

    data_ui = DataUI()

    @pytest.fixture(autouse=True)
    def setup(self, get_driver):
        self.driver = get_driver
        self.main_page = MainSteps(self.driver)
        self.sign_in = SignInSteps(self.driver)
        self.my_account_page = MyAccountSteps(self.driver)
        self.user_bar = UserBarSteps(self.driver)
        self.contact_us_page = ContactUsSteps(self.driver)
        self.filter_page = FilterPage(self.driver)
        self.main_page.open_main_page_url()

    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("Contact us")
    @allure.title("Test 2 - Contact us positive")
    def test_02(self, faker):
        self.user_bar.contact_us_button_click()
        self.contact_us_page.at_page()
        self.contact_us_page.in_subject_heading_list_select_customer_service()
        self.contact_us_page.email_field_input(self.data_ui.USER_EMAIL)
        self.contact_us_page.attach_file_upload(self.data_ui.TXT_FILE)
        self.contact_us_page.message_field_input(faker.text())
        self.contact_us_page.send_button_click()
        self.contact_us_page.at_page()
        self.user_bar.success_alert_check_text(TitleMessages().CONTACT_US_SUCCESSFULY)


    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("Contact us")
    @allure.title("Test 3 - Check required fields in *Contact us* page")
    def test_03(self):
        self.user_bar.contact_us_button_click()
        self.contact_us_page.at_page()
        self.contact_us_page.in_subject_heading_list_select_customer_service()
        self.contact_us_page.email_field_input(self.data_ui.USER_EMAIL)
        self.contact_us_page.attach_file_upload(self.data_ui.TXT_FILE)
        self.contact_us_page.send_button_click()
        self.contact_us_page.at_page()
        self.user_bar.error_alert_check_text(TitleMessages.ONE_ERROR_TITLE,
                                             TitleMessages.MESSAGE_FIELD_EMPTY_ERROR)