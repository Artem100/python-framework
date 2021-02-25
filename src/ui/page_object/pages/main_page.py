import allure

from src.resources.input_data.data_and_params import DataUI
from src.ui.page_object.pages.base_page import BasePage


class MainPage(BasePage):

    TITLE_MAIN_PAGE = "My Store"
    URL_MAIN_PAGE = DataUI().MAIN_PAGE_UI_URL

    @allure.step("*Main* page")
    def at_page(self):
        self.title_page(self.TITLE_MAIN_PAGE)
        return self

    @allure.step("Open *Main* page via URL")
    def open_main_page_via_url(self):
        self.open(self.URL_MAIN_PAGE)
        return self