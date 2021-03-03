import time
from datetime import datetime

import allure
from selenium.webdriver.common.by import By

from src.resources.input_data.data_and_params import log_files
from src.ui.page_object.pages.base_page import BasePage


class FilterPage(BasePage):

    WOMAN_PAGE = "Women - My Store"
    PRODUCT_NAME = (By.CSS_SELECTOR, "ul.product_list>li h5>a", "PRODUCT NAME")

    @allure.step("At *women* page")
    def at_page_women(self):
        self.title_page(self.WOMAN_PAGE)
        return self

    @allure.step("Read names all products in write them to txt file")
    def read_name_all_products_in_list(self):
        date = str(datetime.now().strftime("%d_%m_%Y_%I_%M_%S").lower())+".log"
        path =log_files + date
        list_values = self.read_values_from_elements_and_make_list_text_values(*self.PRODUCT_NAME)
        print(list_values)
        self.count_of_elements(7, *self.PRODUCT_NAME)
        f = open(path, "w+")
        for i in list_values:
            f.write("\n" + str(i))
        f.close()