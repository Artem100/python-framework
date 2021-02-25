import allure

from src.ui.page_object.pages.main_page import MainPage


class MainSteps(MainPage):

    @allure.step("Open *Main* page via url")
    def open_main_page_url(self):
        self.open_main_page_via_url()
        self.at_page()
