import os
import time
from typing import Callable

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.chromium.webdriver import ChromiumDriver as Chromium
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver as Edge
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.safari.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from fenrir import create_logger
from fenrir.config import FenrirConfig


class InvalidWebdriverException(Exception):
    pass


class MaxRetriesException(Exception):
    pass


def webdriver_create(browser: str, opts=None):
    """
    :param browser: str - possible inputs:
    ['Chrome', 'Safari', 'Edge', 'Chromium', 'Firefox, 'Remote']
    :param opts: object
    :return: Instance of a Webdriver of the specified variety from the parameter.
    """
    if opts is None:
        opts = {}

    browser = browser.upper()

    match browser:
        case "CHROME":

            driver = webdriver.Chrome(
                service=Service(), options=opts
            )
        case "CHROMIUM":
            from selenium.webdriver.chrome.service import Service as ChromeService

            return webdriver.Chrome(
                service=ChromeService(),
                options=opts,
            )
        case "FIREFOX":

            driver = webdriver.Firefox(options=opts)
        case "EDGE":
            driver = webdriver.Edge(
                service=Service(), options=opts
            )
        case "SAFARI":
            driver = webdriver.Safari(options=opts)
        case "REMOTE":
            driver = webdriver.Remote(
                command_executor=os.getenv(
                    "FENRIR_REMOTE_WEBDRIVER", "http://localhost:4444"
                ),
                options=opts,
            )
        case _:
            raise InvalidWebdriverException(
                browser,
                f"Specified Driver {browser} is not present in webdriver_manager",
            )
    return driver


class CorePage:
    """
    This Class extends selenium features to behave in a specific way for
        to override some functions that otherwise do not operate the way one
        would expect when testing.
    """

    def __init__(
        self,
        driver: Chrome | Chromium | Edge | Firefox,
        config: FenrirConfig,
        log=create_logger(),
    ):
        self.driver = driver
        self._timeout = config.common.timeout
        self.config = config
        self.log = log

    def get(self, url: str) -> Callable[[WebDriver | WebDriver | WebDriver | WebDriver | WebDriver], bool]:
        self.driver.get(url)
        time.sleep(0.2)
        return expected_conditions.url_changes(url)

    def scroll_to_top(self) -> None:
        scroll = "window.scroll(0, 0);"
        self.log.info(f"Scrolling to bottom of page with script: {scroll}")
        self.driver.execute_script(scroll)

    def scroll_to_bottom(self) -> None:
        scroll = "window.scrollTo(0,document.body.scrollHeight)"
        self.log.info(f"Scrolling to bottom of page with script: {scroll}")
        self.driver.execute_script(scroll)

    def find_element(self, by: By, selector: str) -> WebElement:
        """
        Contains timeout and catch StaleElementReference Exceptions
        because that exception is more of an interference than a helpful error.

        :Param: by: By - from selenium.webdriver.common.by import By
        :Param: selector: str - Should be the selector for your element.
        """
        if not os.getenv("CI"):
            time.sleep(0.1)
        try:
            self.log.info(f"{by}: {selector}")
            WebDriverWait(self.driver, timeout=self._timeout).until(
                expected_conditions.visibility_of_element_located((str(by), selector))
            )
            return self.driver.find_element(by, selector)
        except StaleElementReferenceException:
            return self.find_element(by=by, selector=selector)

    def find_elements(self, by: By, selector: str) -> list[WebElement]:
        """
        :param: by: By - from selenium.webdriver.common.by import By
        :param: selector: str - Should be the selector for your element.
        """
        if not os.getenv("CI"):
            time.sleep(0.1)
        try:
            self.log.info(f"{by}: {selector}")
            WebDriverWait(driver=self.driver, timeout=self._timeout).until(
                expected_conditions.presence_of_all_elements_located((str(by), selector))
            )
            return self.driver.find_elements(by=by, value=selector)
        except StaleElementReferenceException:
            return self.driver.find_elements(by=by, value=selector)
