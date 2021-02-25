import allure
from selenium.webdriver.common.by import By

from src.ui.page_object.pages.base_page import BasePage


class UserBarPage(BasePage):

    NAME_PROFILE = (By.CSS_SELECTOR, "div.header_user_info span", "NAME PROFILE")
    SIGN_IN_BUTTON = (By.CSS_SELECTOR, "a.login", "SIGN IN BUTTON")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a.logout", "LOGOUT BUTTON")
    CONTACT_US_BUTTON = (By.CSS_SELECTOR, "a[title='Contact us']", "CONTACT US BUTTON")
    WOMEN_BUTTON = (By.CSS_SELECTOR, "a[title='Women']", "WOMEN BUTTON")
    ALERT_SUCCESS = (By.CSS_SELECTOR, "p.alert-success", "ALERT SUCCESS")
    # ALERT ERROR
    ALERT_ERROR_TITLE = (By.CSS_SELECTOR, "div.alert-danger>p", "ALERT ERROR")
    ALERT_ERROR_TEXT = (By.CSS_SELECTOR, "div.alert-danger li", "ALERT ERROR TEXT")


    @allure.step("Name profile check text")
    def name_profile_check_value(self, text):
        self.check_text_in_element(text, *self.NAME_PROFILE)
        return self

    @allure.step("*Sign In* button click")
    def sign_in_button_click(self):
        self.click(*self.SIGN_IN_BUTTON)
        return self

    @allure.step("Logout button is displayed")
    def logout_button_display(self):
        self.displayed_element(*self.LOGOUT_BUTTON)
        return self

    @allure.step("*Contact us* button click")
    def contact_us_button_click(self):
        self.click(*self.CONTACT_US_BUTTON)
        return self

    @allure.step("Success alert")
    def success_alert_check_text(self, text):
        # self.check_text_in_element(text, *self.ALERT_SUCCESS)
        self.check_text_in_icons_or_messages(text, *self.ALERT_SUCCESS)
        return self

    @allure.step("Error alert")
    def error_alert_check_text(self, text_title, text_message):
        self.check_text_in_element(text_title, *self.ALERT_ERROR_TITLE)
        self.check_text_in_element(text_message, *self.ALERT_ERROR_TEXT)
        return self

    @allure.step("*Women* button click")
    def women_button_click(self):
        self.click(*self.WOMEN_BUTTON)
        return self
