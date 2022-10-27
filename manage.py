from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
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
        # Check if string is url regex


        geckodriver_autoinstaller.install()
        # Check if the current version of geckodriver exists
        # and if it doesn't exist, download it automatically,
        # then add geckodriver to path
        firefox_options = Options()
        # firefox_options.add_argument("--headless")
        self._driver = webdriver.Firefox(options=firefox_options)
        self._driver.implicitly_wait(10)
        self._driver.get(source)

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

    def count_classes(self, class_name, number=1):
        pass

    @staticmethod
    def has_attribute(self, selenium_obj, attribute_name: str | tuple) -> bool:
        pass

    @staticmethod
    def check_attribute_value(self, selenium_obj, **attributes) -> bool:
        pass

    def __del__(self):
        self._driver.close()

    """
    3. გადაიყვანს HTML-ს სელენიუმის ობიექტად
    4. ამ ობიექტზე შესაძლებლობა უნდა გვქონდეს შემდეგი მეთოდების გადატარების:
    """

    """
    შეამოწმე დავალებაში არის თუ არა შექმნილი 3 user კლასის ელემენტი რომელთაც ატრიბუტებში აქვთ style="color: red;"
    
    sypter = Sypter(source)
    assert sypter.if_exists_by_class(classname="user", number=3)
    
    for user in selenium_objs_of_user:
      assert check_attribute_value(user, style="color: red;")
    """


if __name__ == "__main__":
    sypter = Sypter('https://www.w3schools.com/html/tryit.asp?filename=tryhtml_id_css')
    print(sypter.if_exists_by_id("iframe"))

    sypter = Sypter('https://davidunilab.github.io/davidunilab.front-lesson12/')
    # TRUTH
    print(sypter.if_exists_by_class("paragraph", number=2))
    print(sypter.if_exists_by_class("paragraph", min_num=2))
    print(sypter.if_exists_by_class("paragraph", max_num=2))
    print(sypter.if_exists_by_class("paragraph", min_num=2, max_num=2))
    print(sypter.if_exists_by_class("paragraph", min_num=1, max_num=2))
    print(sypter.if_exists_by_class("paragraph", min_num=0, max_num=2))
    print(sypter.if_exists_by_class("paragraph", number=2, min_num=1, max_num=2))
    print(sypter.if_exists_by_class("paragraph", number=2, min_num=2, max_num=2))

    # FALSE
    print(sypter.if_exists_by_class("paragraph", number=1))




