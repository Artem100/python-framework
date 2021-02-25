import logging
from faker import Faker
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.errorhandler import ErrorHandler
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def format_selector(by, locator, name=None):
	selector = (by, locator)
	name = name if name else selector
	return selector, name


class BasePage(object):
	def __init__(self, driver):
		self.driver = driver

	LOGGER = logging.getLogger(__name__)
	faker = Faker()

	driver = None
	timeout = 5

	LOADING_ICON = (By.CSS_SELECTOR, "span.loader", "LOADING ICON")


	def timeout_element_error(self, selector, name):
		""" Timeout Webdriver and NoSuchElementException"""
		BasePage.LOGGER.error("Timeout - < {1} > element not found: {0} \n".format(selector, name))
		raise Exception("Timeout - < {1} > element not found: {0}".format(selector, name))

	# AssertionError
	def element_doesnt_contain_expected_value_error(self, name, value, result):
		BasePage.LOGGER.error("Element < {0} > doesn't contain expected value.\nExpected value: {1}\nActual value: {2}".format(name, value, result))
		raise AssertionError("Element < {0} > doesn't contain expected value. \nExpected value: {1},\nActual value: {2}".format(name, value, result))

	def cant_click_on_the_element_error(self, selector, name):
		"""ErrorHandler, ElementClickInterceptedException"""
		BasePage.LOGGER.error("Can't click on {0} element: {1}".format(name, selector))
		assert Exception("Can't click on {0} element: {1}".format(name, selector))

	# WebDriverWait
	def element_isnt_display_on_page(self, selector, name):
		BasePage.LOGGER.error(
			"WebDriverWait exception: Element < {1} > isn't displayed: {0} on page".format(selector, name))
		assert Exception("WebDriverWait exception: Element < {1} > isn't displayed: {0} on page".format(selector, name))

	def open(self, url):
		BasePage.LOGGER.info("Open page by url < {} >".format(url))
		self.driver.get(url)

	def close(self):
		self.driver.close()

	def delete_cookies(self):
		self.driver.delete_all_cookies()

	# UI elements like titles or icons
	def find_element_located(self, selector, name):
		try:
			element = WebDriverWait(self.driver, BasePage.timeout).until(EC.presence_of_element_located(selector))
			return element
		except (TimeoutException, NoSuchElementException):
			self.timeout_element_error(selector, name)
		except ErrorHandler:
			self.cant_click_on_the_element_error(selector, name)

	# UI elements like buttons
	def find_element_clickable(self, selector, name):
		try:
			element = WebDriverWait(self.driver, BasePage.timeout).until(EC.element_to_be_clickable(selector))
			return element
		except (TimeoutException, NoSuchElementException):
			self.timeout_element_error(selector, name)
		except ErrorHandler:
			self.cant_click_on_the_element_error(selector, name)

	def find_elements_visibility(self, selector, name):
		self.LOGGER.info("Find elements < {} > ".format(name))
		try:
			elements = WebDriverWait(self.driver, BasePage.timeout).until(EC.visibility_of_all_elements_located(selector))
			return elements
		except (TimeoutException, NoSuchElementException):
			self.timeout_element_error(selector, name)
		except ErrorHandler:
			self.cant_click_on_the_element_error(selector, name)

	def click(self, *selector):
		selector, name = format_selector(*selector)
		element = self.find_element_clickable(selector, name)
		self.LOGGER.info("Click on < {} >".format(name))
		try:
			element.click()
		except Exception as e:
			BasePage.LOGGER.warning(
				"Test can't click on element < {0} >\n < {1} > \n < {2} >".format(name, selector, e))
			raise Exception("Test can't click on element < {0} >\n < {1} > \n < {2} >".format(name, selector, e))
		# except ErrorHandler:
		# 	element.click()

	def enter_text(self, key_send, *selector):
		selector, name = format_selector(*selector)
		element = self.find_element_clickable(selector, name)
		self.LOGGER.info("Input text value:* {} * to < {} > element.".format(key_send, name))
		try:
			element.send_keys(key_send)
		except Exception as e:
			BasePage.LOGGER.warning("Test input text to element < {0} >\n < {1} > \n < {2} >".format(name, selector, e))
			raise Exception("Test can't input text to element < {0} >\n < {1} > \n < {2} >".format(name, selector, e))

	def title_page(self, page_title):
		current_page = self.driver.title
		try:
			self.LOGGER.info("Check TITLE of page < {} > ".format(page_title))
			current_page = WebDriverWait(self.driver, BasePage.timeout).until(EC.title_contains(page_title))
			self.LOGGER.info("------< {} > page------".format(page_title))
		except AssertionError:
			BasePage.LOGGER.error(f"\nCurrent title of page doesn't compare with expected title.\nExpected title: {page_title}\nActual title: {current_page}")
			raise AssertionError(f"\nCurrent title of page doesn't compare with expected title.\nExpected title: {page_title}\nActual title: {current_page}")
		except TimeoutException:
			BasePage.LOGGER.error(f"\nCurrent title of page doesn't compare with expected title.\nExpected title: {page_title}\nActual title: {current_page}")
			raise AssertionError(f"\nCurrent title of page doesn't compare with expected title.\nExpected title: {page_title}\nActual title: {current_page}")

	def displayed_element(self, *selector):
		selector, name = format_selector(*selector)
		element = self.find_element_located(selector, name)
		self.LOGGER.info("Check that element < {} > is displayed on page".format(name))
		try:
			element.is_displayed()
		except AssertionError as e:
			BasePage.LOGGER.error("Element < {0} > is displayed on page. {1} \n{2}}".format(name, selector, e))
			raise AssertionError("Element < {0} > is displayed on page. {1} \n{2}}".format(name, selector, e))
