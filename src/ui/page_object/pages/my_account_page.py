import allure
from selenium.webdriver.common.by import By

from src.ui.page_object.pages.base_page import BasePage


class MyAccountPage(BasePage):

    TITLE_MY_ACCOUNT_PAGE = "My account - My Store"
    RETURN_TO_HOME_BUTTON = (By.CSS_SELECTOR, "a[title='Return to Home']", "RETURN TO HOME BUTTON")


    @allure.step("*My account* page")
    def at_page(self):
        self.title_page(self.TITLE_MY_ACCOUNT_PAGE)
        return self

    @allure.step("*Return to home* button is displayed")
    def return_home_button_display(self):
        self.displayed_element(*self.RETURN_TO_HOME_BUTTON)
        return self