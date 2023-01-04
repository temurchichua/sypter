import os

import logging
from fnmatch import fnmatch

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import geckodriver_autoinstaller

# TODO: import version from pyproject.toml
__version__ = "0.0.2"

logging.basicConfig(level=logging.INFO)

class Sypter:
    """
    This is the base class for Frontend Testing Framework the Sypter

    It wraps selenium and adds testing functionalities
    """

    def __init__(self, source=None):
        """
        source could be one of three:
        - string HTML
        - url
        - local_file HTML
        """
        self._driver = None
        self.source = source
        self.source_type = None

        self.config_driver()

        if source is not None:
            self.process_source(source)

        else:
            logging.warning("Initiated Sypter without source. Please use process_source() to process source later")

    def config_driver(self, **kwargs):
        """
        Configure driver
        """
        # Try to get Chrome driver
        try:
            from selenium.webdriver.chrome.options import Options

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            self._driver = webdriver.Chrome(options=chrome_options)
            self._driver.implicitly_wait(10)
        # if not installed try Firefox driver
        except Exception:
            # Check if the current version of geckodriver exists
            # and if it doesn't exist, download it automatically,
            # then add geckodriver to path
            # TODO: this should be done one time when the package is installed
            geckodriver_autoinstaller.install()

            from selenium.webdriver.firefox.options import Options

            firefox_options = Options()
            firefox_options.add_argument("--headless")
            self._driver = webdriver.Firefox(options=firefox_options)
            self._driver.implicitly_wait(10)

        for key, value in kwargs.items():
            self._driver.__setattr__(key, value)

    def process_source(self, source):
        """
        Process source and return source type
        """
        self.source = source
        self._get_source_type()

        if self.source_type == "url":
            self._driver.get(source)
        elif self.source_type == "file":
            self._driver.get(f"file://{source}")
        elif self.source_type == "html":
            self._driver.get(f"data:text/html;charset=utf-8,{source}")

    def _get_source_type(self):
        """
        Check if source is url, file or html
        """
        import re

        source = self.source.strip()
        url_regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        # Check if source is url
        if re.match(url_regex, source):
            self.source_type = 'url'
        # else if source is a string containing html
        elif source.startswith('<') and source.endswith('>'):
            self.source_type = 'html'
        # else if source is a file
        elif os.path.isfile(source):
            # check if file exists
            if not os.path.exists(source):
                raise ValueError("File does not exist")
            elif os.path.isfile(source):
                self.source_type = "file"
            else:
                raise ValueError("Invalid source")

    @staticmethod
    def check_elements_quantity(elements, comparison_operator: str, numeric_value) -> bool:
        """
        Check if elements quantity is valid
        :param elements: elements to check
        :param comparison_operator: comparison operator "<", ">", "<=", ">=", "==", "!="
        :param numeric_value: numeric value to compare with (second operand)
        :return:
        """
        number_of_elements = len(elements)  # first operand

        # write switch cases
        match comparison_operator:
            case "<":
                return number_of_elements < numeric_value
            case ">":
                return number_of_elements > numeric_value
            case "<=":
                return number_of_elements <= numeric_value
            case ">=":
                return number_of_elements >= numeric_value
            case "==":
                return number_of_elements == numeric_value
            case "!=":
                return number_of_elements != numeric_value
            case _:
                raise ValueError("Invalid comparison operator")

    @staticmethod
    def get_selector(selector_type: str, selector_value: str) -> tuple:
        """
        Get selector type and selector value
        """
        selector_type = selector_type.lower()
        if selector_type == "id":
            return By.ID, selector_value
        elif selector_type == "class":
            return By.CLASS_NAME, selector_value
        elif selector_type == "tag":
            return By.TAG_NAME, selector_value
        elif selector_type == "css":
            return By.CSS_SELECTOR, selector_value
        elif selector_type == "xpath":
            return By.XPATH, selector_value
        else:
            raise ValueError("Invalid selector type")

    def test(self, selector_value: str, selector_type: str = "tag",
             comparison_operator: str = "==", numeric_value: int = 1,
             style_tests: list = None, attribute_tests: list = None) -> list:
        """
        Test HTML element
        """

        # get selector
        selector = self.get_selector(selector_type, selector_value)

        # get elements
        try:
            elements = self._driver.find_elements(*selector)
        except NoSuchElementException:
            raise False

        # check if attributes need to be filtered
        if attribute_tests is not None:
            if isinstance(attribute_tests, list) and attribute_tests[0].get("attribute_name"):
                attribute_tests = {attribute_test["attribute_name"]: attribute_test["attribute_value"]
                                   for attribute_test in attribute_tests}

            elements = self.filter_elements_by_attributes(elements, attribute_tests)

        # check if styles need to be filtered
        if style_tests is not None:
            if isinstance(style_tests, list) and style_tests[0].get("attribute_name"):
                style_tests = {style_test["attribute_name"]: style_test["attribute_name"] for style_test in style_tests}
            elements = self.filter_elements_by_style(elements, style_tests)

        return self.check_elements_quantity(elements, comparison_operator, numeric_value)

    @staticmethod
    def filter_elements_by_attributes(elements, attributes: dict) -> list:
        """
        Check if there are elements with given css selector and attributes
        """
        # filter list of elements to get only elements with given attributes
        for attribute, value in attributes.items():
            elements = [element for element in elements
                        if element.get_attribute(attribute) and fnmatch(element.get_attribute(attribute), value)]

        return elements

    @staticmethod
    def filter_elements_by_style(elements, styles: dict) -> list:
        """
        Filter elements by css style attribute

        :param styles: dictionary of styles to filter by
        :param elements: list of elements to filter
        :return: list of elements
        """
        # filter list of elements to get only elements with given styles
        for style, value in styles.items():
            elements = [element for element in elements if fnmatch(element.value_of_css_property(style), value)]

        return elements
