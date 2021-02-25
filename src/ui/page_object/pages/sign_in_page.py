import allure
from selenium.webdriver.common.by import By

from src.ui.page_object.pages.base_page import BasePage


class SignInPage(BasePage):

    TITLE_SIGN_IN = "Login - My Store"
    EMAIL_FIELD = (By.CSS_SELECTOR, "#email", "EMAIL FIELD")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "#passwd", "PASSWORD FIELD")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button#SubmitLogin", "SUBMIT BUTTON")

    @allure.step("*SignIn* Page")
    def at_page(self):
        self.title_page(self.TITLE_SIGN_IN)
        return self

    @allure.step("Email field input value")
    def email_field_input_value(self, text):
        self.enter_text(text, *self.EMAIL_FIELD)
        return self

    @allure.step("Password field input value")
    def password_field_input_value(self, text):
        self.enter_text(text, *self.PASSWORD_FIELD)
        return self

    @allure.step("Submit Login button click")
    def submitlogin_button_click(self):
        self.click(*self.SUBMIT_BUTTON)
        return self



