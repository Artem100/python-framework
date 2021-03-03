import logging
from faker import Faker
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidArgumentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.errorhandler import ErrorHandler
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

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


	def read_values_from_elements_and_make_list_text_values(self, *selector):
		""""
		Create list from text values of list elements, than check text_value on occurrence in list
		"""""
		selector, name = format_selector(*selector)
		elements = self.find_elements_visibility(selector, name)
		try:
			self.LOGGER.info("Read values from elements < {} > and save values in list".format(name))
			values = []
			for value in elements:
				values.append(value.text)
			return values
		except Exception as e:
			BasePage.LOGGER.warning("Test can't Read values from elements < {0} >. {1} \n{2}".format(name, selector, e))
			raise Exception("Test can't Read values from elements < {0} >. {1} \n{2}".format(name, selector, e))

	def count_of_elements(self, count, *selector):
		selector, name = format_selector(*selector)
		elements = self.find_elements_visibility(selector, name)
		self.LOGGER.info("Check count of < {} > elements".format(name))
		try:
			assert len(elements) == int(count)
		except AssertionError:
			BasePage.LOGGER.error(
				"Count value doesn't match with test in element < {0} >.\nActual result: {1}\nExpected result: {2}".format(
					name, len(elements), count))
			raise AssertionError(
				"Count value doesn't match with test in element < {0} >.\nActual result: {1}\nExpected result: {2}".format(
					name, len(elements), count))


	def select_value_in_dropdown_by_option_visible_text(self, text, *selector):
		selector, name = format_selector(*selector)
		element = Select(self.find_element_located(selector, name))
		self.LOGGER.info(f"Select value < {text} > from the list *{selector}*")
		try:
			element.select_by_visible_text(text)
		except Exception as e:
			BasePage.LOGGER.warning(f"Test couldn't select value by text: < {text} > in the list: {selector}")
			raise Exception(f"Test couldn't select value by text: < {text} >  in the list: {selector}")

	def backspace_button_all(self, *selector):
		selector, name = format_selector(*selector)
		element = self.find_element_clickable(selector, name)
		self.LOGGER.info("Clear text field < {} > use the BASCKSPACE button".format(name))
		try:
			length = len(element.get_attribute('value'))
			element.send_keys(length * Keys.BACKSPACE)
		except TypeError:
			BasePage.LOGGER.warning("Field is clear already")
		except Exception as e:
			BasePage.LOGGER.warning(
				"Test can't clear text in < {0} > field use the BASCKSPACE button. {1} \n{2}".format(name, selector, e))
			raise Exception(
				"Test can't clear text in < {0} > field use the BASCKSPACE button. {1} \n{2}".format(name, selector, e))

	def upload_file(self, path, *selector):
		selector, name = format_selector(*selector)
		element = self.find_element_located(selector, name)
		self.LOGGER.info("Upload file by path : * {} * to < {} > element.".format(path, name))
		try:
			element.send_keys(path)
		except InvalidArgumentException as e:
			BasePage.LOGGER.warning(f"Test can't find file in project by path: < {path} >\n{e}")
			raise Exception(f"Test can't find file in project by path: < {path} >\n{e}")
		except Exception as e:
			BasePage.LOGGER.warning("Test can't upload image to element < {0} >\n < {1} > \n < {2} >".format(name, selector, e))
			raise Exception("Test can't upload image to element < {0} >\n < {1} > \n < {2} >".format(name, selector, e))
