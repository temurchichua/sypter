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

        geckodriver_autoinstaller.install()
        # Check if the current version of geckodriver exists
        # and if it doesn't exist, download it automatically,
        # then add geckodriver to path

        firefox_options = Options()
        # firefox_options.add_argument("--headless")
        self._driver = webdriver.Firefox(options=firefox_options)
        self._driver.implicitly_wait(10)

        self.source_type = self._get_source_type(source)
        if self.source_type == "url":
            self._driver.get(source)
        elif self.source_type == "file":
            self._driver.get(f"file://{source}")
        elif self.source_type == "html":
            self._driver.get(f"data:text/html;charset=utf-8,{source}")

        self._driver.get(source)

    # შეიძლება ამის ცალკე გატანაც
    def _get_source_type(self, source):
        import re
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
            # Check if string is local file
            import os
            if os.path.isfile(source):
                return "file"
            # Check if string is HTML
            elif source.startswith('<') and source.endswith('>'):
                return "html"
            else:
                raise ValueError("Invalid source")

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
    # sypter = Sypter('https://www.w3schools.com/html/tryit.asp?filename=tryhtml_id_css')
    # print(sypter.if_exists_by_id("iframe"))
    #
    # sypter = Sypter('https://davidunilab.github.io/davidunilab.front-lesson12/')
    # # TRUTH
    # print(sypter.if_exists_by_class("paragraph", number=2))
    # print(sypter.if_exists_by_class("paragraph", min_num=2))
    # print(sypter.if_exists_by_class("paragraph", max_num=2))
    # print(sypter.if_exists_by_class("paragraph", min_num=2, max_num=2))
    # print(sypter.if_exists_by_class("paragraph", min_num=1, max_num=2))
    # print(sypter.if_exists_by_class("paragraph", min_num=0, max_num=2))
    # print(sypter.if_exists_by_class("paragraph", number=2, min_num=1, max_num=2))
    # print(sypter.if_exists_by_class("paragraph", number=2, min_num=2, max_num=2))
    #
    # # FALSE
    # print(sypter.if_exists_by_class("paragraph", number=1))

    html = """
        data:text/html;charset=utf-8,
        <div class="post-signature owner flex--item">
            <div class="user-info user-hover">
            <div class="user-action-time">
                asked <span title="2021-12-09 12:02:00Z" class="relativetime">38 mins ago</span>
            </div>
            <div class="user-gravatar32">
                <a href="/users/4094231/umair-ayub"><div class="gravatar-wrapper-32"><img src="https://www.gravatar.com/avatar/da5d12e4b0c319022432a23fc5344831?s=64&amp;d=identicon&amp;r=PG&amp;f=1" alt="" width="32" height="32" class="bar-sm"></div></a>
            </div>
            <div class="user-details" itemprop="author" itemscope="" itemtype="http://schema.org/Person">
                <a href="/users/4094231/umair-ayub">Umair Ayub</a><span class="d-none" itemprop="name">Umair Ayub</span>
                <div class="-flair">
                    <span class="reputation-score" title="reputation score 14,591" dir="ltr">14.6k</span><span title="12 gold badges" aria-hidden="true"><span class="badge1"></span><span class="badgecount">12</span></span><span class="v-visible-sr">12 gold badges</span><span title="61 silver badges" aria-hidden="true"><span class="badge2"></span><span class="badgecount">61</span></span><span class="v-visible-sr">61 silver badges</span><span title="131 bronze badges" aria-hidden="true"><span class="badge3"></span><span class="badgecount">131</span></span><span class="v-visible-sr">131 bronze badges</span>
                </div>
            </div>
        </div>
        </div>
    """

    Sypter(html)
