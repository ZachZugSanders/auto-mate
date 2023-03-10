import logging
from os import environ

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait

timeout = wait_timeout = 10


class InvalidWebdriverException(Exception):

    def __int__(self, message):
        self.message = message
        super().__init__(self.message)


def webdriver_create(which_driver: str, opts=None):
    """
    :param which_driver: str - possible inputs: ['Chrome', 'Safari', 'Edge', 'Chromium', 'Firefox']
    :param opts: object
    :return: Instance of a Webdriver of the specified variety from the parameter.
    """
    if opts is None:
        opts = {}
    from selenium import webdriver
    which_driver = which_driver.upper()

    match which_driver:
        case 'CHROME':
            from webdriver_manager.chrome import ChromeDriverManager
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        case 'CHROMIUM':
            from selenium.webdriver.chrome.service import Service as ChromeService
            from webdriver_manager.chrome import ChromeDriverManager
            from webdriver_manager.chrome import ChromeType
            return webdriver.Chrome(
                service=ChromeService(ChromeDriverManager(
                    chrome_type=ChromeType.CHROMIUM).install()), options=opts)
        case 'FIREFOX':
            from webdriver_manager.firefox import GeckoDriverManager
            driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()), options=opts)
        case 'EDGE':
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=opts)
        case 'SAFARI':
            driver = webdriver.Safari(options=opts)
        case _:
            raise InvalidWebdriverException(which_driver,
                                            f'Specified Driver {which_driver} is not present in webdriver_manager')
    driver.implicitly_wait(10)
    return driver


class CorePage:
    """
    This Class extends selenium features to behave in a specific way for to override some functions that otherwise do
    not operate the way one would expect when testing.
    """

    def __init__(self, driver: Chrome | Chromium | Edge | Firefox, config: FenrirConfig):
        self.driver = driver
        self._timeout = config.common.timeout
        self.config = config

    def get(self, url: str):
        return self.driver.get(url)

    def scroll_to_top(self) -> None:
        self.driver.execute_script("window.scroll(0, 0);")

    def scroll_to_bottom(self) -> None:
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def find_element(self, by: By, selector: str) -> WebElement:
        """
        Adding timeouts and catch a really stupid StaleElementReference Exceptions
        because that is not something that would ever interfere with the operation of a test.
        a normal web-application it just makes dynamically changed elements short circuit the whole test.
        :Param: by: By - from selenium.webdriver.common.by import By
        :Param: selector: str - Should be the selector for your element.
        """
        try:
            WebDriverWait(self.driver, timeout=self._timeout).until(
                expected_conditions.visibility_of_element_located((by, selector))
            )
            return self.driver.find_element(by, selector)
        except StaleElementReferenceException:
            WebDriverWait(self.driver, timeout=self._timeout).until(
                expected_conditions.visibility_of_element_located((by, selector))
            )
            return self.driver.find_element(by, selector)

    def find_elements(self, by: By, selector: str) -> list[WebElement]:
        return self.driver.find_elements(by=by, value=selector)

