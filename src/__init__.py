from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import geckodriver_autoinstaller


class Sypter:
    """
    This is the base class for Frontend Testing Framework the Sypter

    It wraps selenium and adds testing functionalities
    """

    def __init__(self, source):
        """
        source could be one of three:
        - string HTML
        - url
        - local_file HTML
        """
        self.source = source
        # Check if the current version of geckodriver exists
        # and if it doesn't exist, download it automatically,
        # then add geckodriver to path
        geckodriver_autoinstaller.install()

        # Try to get firefox driver
        # if not installed try chrome driver
        try:
            from selenium.webdriver.firefox.options import Options

            firefox_options = Options()
            firefox_options.add_argument("--headless")
            self._driver = webdriver.Firefox(options=firefox_options)
            self._driver.implicitly_wait(10)
        except Exception:
            from selenium.webdriver.chrome.options import Options

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            self._driver = webdriver.Chrome(options=chrome_options)
            self._driver.implicitly_wait(10)


        self.source_type = self._get_source_type()
        if self.source_type == "url":
            self._driver.get(source)
        elif self.source_type == "file":
            self._driver.get(f"file://{source}")
        elif self.source_type == "html":
            self._driver.get(f"data:text/html;charset=utf-8,{source}")

    # it may be externalized
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
        if re.match(url_regex, source):
            return 'url'
        else:
            # Check if string is HTML
            if source.startswith('<') and source.endswith('>'):
                return "html"
            # Check if string is local file
            import os
            # check if file exists
            if not os.path.exists(source):
                raise ValueError("File does not exist")
            elif os.path.isfile(source):
                return "file"
            else:
                raise ValueError("Invalid source")

    def if_exists_by_css(self, css_selector) -> bool:
        """
        Check if element exists by css selector
        """
        try:
            self._driver.find_element(By.CSS_SELECTOR, css_selector)
            return True
        except NoSuchElementException:
            return False

    def if_exists_by_id(self, element_id: str) -> bool:
        """
        check if html element has given id
        """
        try:
            self._driver.find_element(By.ID, element_id)
            return True
        except NoSuchElementException:
            return False

    def if_exists_by_class(self, class_name, number=1, min_num=None, max_num=None) -> bool:
        """
        check existence of class in HTML element
        """
        minimum, maximum, class_count = False, False, False
        try:
            elements = self._driver.find_elements(By.CLASS_NAME, class_name)
        except NoSuchElementException:
            return False

        if elements:
            count = len(elements)
            if min_num:
                minimum = min_num <= count
            if max_num:
                maximum = max_num >= count
            if number:
                class_count = number == count

        if minimum and maximum and class_count:
            return True
        elif min_num and max_num:
            return minimum and maximum
        elif min_num and number > 1:
            return minimum and class_count
        elif max_num and number > 1:
            return maximum and class_count
        elif min_num:
            return minimum
        elif max_num:
            return maximum
        elif number:
            return class_count

    def check_attribute_value_by_css(self, css_selector, **attributes) -> bool:
        """
        Check if attribute value is equal to given value
        """

        # if element does not exist, it will raise exception
        element = self._driver.find_element(By.CSS_SELECTOR, css_selector)

        for attribute, value in attributes.items():
            if element.get_attribute(attribute) != value:
                return False
        return True

    def check_if_attribute_exists_by_css(self, css_selector, attribute_name: str | tuple) -> bool:
        element = self._driver.find_element(By.CSS_SELECTOR, css_selector)
        if isinstance(attribute_name, tuple):
            for attr in attribute_name:
                if not element.get_attribute(attr):
                    return False
        else:
            if not element.get_attribute(attribute_name):
                return False
        return True


if __name__ == "__main__":
    pass
