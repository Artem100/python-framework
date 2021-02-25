import logging

from sys import platform
from os.path import dirname, abspath
from os import getenv

import allure
import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.edge.webdriver import WebDriver

LOGGER = logging.getLogger(__name__)
ROOT_DIR = dirname(abspath(__file__))
DRIVERS_DIR = ROOT_DIR + "//src//ui//drivers"
DOWNLOAD_DIR = ROOT_DIR + "//download_files"

@pytest.fixture(scope="session")
def get_driver(request):
    jenkins = getenv('JENKINS_HOME')
    browser_list = request.config.getoption("--browser")

    chrome_driver_path = ""
    firefox_driver_path = ""

    if platform == "linux" or platform == "linux2":
        chrome_driver_path = DRIVERS_DIR + "//linux//chromedriver"
        firefox_driver_path = DRIVERS_DIR + "//linux//geckodriver"
    elif platform == "darwin":
        chrome_driver_path = DRIVERS_DIR + "//mac//chromedriver"
        firefox_driver_path = DRIVERS_DIR + "//src//ui//drivers//mac//geckodriver"
    elif platform == "win32":
        chrome_driver_path = DRIVERS_DIR + "//windows//chromedriver.exe"
        firefox_driver_path = DRIVERS_DIR + "//windows//geckodriver.exe"

    if 'chrome' in browser_list:
        options = webdriver.ChromeOptions()
        preferences = {"download.default_directory": DOWNLOAD_DIR}
        options.add_argument("--start-maximized")
        options.add_experimental_option("prefs", preferences)
        capabilities = options.to_capabilities()
        if jenkins:
            options.add_argument('--headless')
            options.add_argument("--window-size=1920,1080")
        print(ROOT_DIR + chrome_driver_path)
        driver = webdriver.Chrome(executable_path=chrome_driver_path, desired_capabilities=capabilities)
    elif 'firefox' in browser_list:
        fp = webdriver.FirefoxProfile()
        fp_options = webdriver.FirefoxOptions()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference('browser.download.dir', DOWNLOAD_DIR)
        fp.set_preference("browser.helperApps.alwaysAsk.force", False)
        fp.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/pdf,application/x-pdf')
        fp.set_preference("pdfjs.disabled", True)
        # driver = webdriver.Firefox(executable_path=ROOT_DIR + firefox_driver, firefox_profile=fp)
        driver = webdriver.Firefox(executable_path=firefox_driver_path, firefox_profile=fp)
        driver.maximize_window()
    elif 'edge' in browser_list:
        driver: WebDriver = webdriver.Edge()
    LOGGER.info('Test run with *{0}* browser.'.format(browser_list))
    driver.set_script_timeout(60)
    yield driver
    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Type of browser: edge, chrome, firefox")



@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    marker = item.get_closest_marker("ui")
    if marker:
        if rep.when == "call" and rep.failed:
            try:
                allure.attach(item.instance.driver.get_screenshot_as_png(),
                              name=item.name,
                              attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print(e)

@pytest.fixture(scope="function")
def faker():
    return Faker()

