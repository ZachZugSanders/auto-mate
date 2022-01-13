import logging
import os
from os import environ

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait

wait_timeout = os.getenv('WEBDRIVER_TIMEOUT')


class BaseEndpoint:
    def __init__(self, site: str = environ.get('SITE')):
        self.site = site
        assert self.site

    def build_endpoint(self, endpoint: str, extra_ending: str = None):
        if endpoint and extra_ending is None:
            built_endpoint = f"{self.site}/api/{endpoint}"
            logging.info('\n : Endpoint built for request:' + built_endpoint + '\n')
            return built_endpoint
        elif endpoint and extra_ending is not None:
            built_endpoint = f"{self.site}/api/{endpoint}/{extra_ending}"
            logging.info('\n : Endpoint built for request with extra ending:' + built_endpoint + '\n')
            return built_endpoint
        else:
            raise Exception('Endpoint does not have a value.')


def driver_choice(which_driver: str):
    """
    :return: Webdriver.exe
    """
    from selenium import webdriver
    which_driver = which_driver.upper()
    if which_driver == 'CHROME':
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif which_driver == 'CHROMIUM':
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.utils import ChromeType
        driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    elif which_driver == 'FIREFOX':
        from webdriver_manager.firefox import GeckoDriverManager
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif which_driver == 'INTERNETEXPLORER':
        logging.warning("You mother fucker, seriously?!")
        from webdriver_manager.microsoft import IEDriverManager
        driver = webdriver.Ie(IEDriverManager().install())
    elif which_driver == 'EDGE':
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    elif which_driver == 'OPERA':
        from webdriver_manager.opera import OperaDriverManager
        driver = webdriver.Opera(executable_path=OperaDriverManager().install())
    else:
        logging.error('Specified Driver is not present in webdriver_manager')
        raise NotImplementedError(which_driver)
    return driver


class CorePage(object):
    """
    Class which will wait for elements to appear. Once the web element has appeared
    operations may be performed upon them.
    """
    def __init__(self, driver):
        self.driver = driver

    def by_name(self, name_selector):
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.NAME, name_selector))
            )
            return self.driver.find_element(By.NAME, name_selector)
        except StaleElementReferenceException:
            self.driver.implicity_wait(10)
            WebDriverWait(self.driver, wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.NAME, name_selector))
            )
            return self.driver.find_element(By.NAME, name_selector)

    def by_id(self, id_selector):
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.ID, id_selector)))
            return self.driver.find_element(By.ID, id_selector)
        except StaleElementReferenceException:
            self.driver.implicity_wait(10)
            WebDriverWait(self.driver, wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.ID, id_selector)))
            return self.driver.find_element(By.ID, id_selector)

    def by_class_name(self, class_name_selector):
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, class_name_selector)))
            return self.driver.find_element(By.CLASS_NAME, class_name_selector)
        except StaleElementReferenceException:
            self.driver.implicity_wait(10)
            WebDriverWait(self.driver, wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, class_name_selector)))
            return self.driver.find_element(By.CLASS_NAME, class_name_selector)

    def by_css_selector(self, css_selector):
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
            return self.driver.find_element(By.CSS_SELECTOR, css_selector)
        except StaleElementReferenceException:
            self.driver.implicity_wait(10)
            WebDriverWait(self.driver, wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
            return self.driver.find_element(By.CSS_SELECTOR, css_selector)

    def by_xpath(self, xpath_query):
        try:
            WebDriverWait(self.driver, wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.XPATH, xpath_query))
            )
            return self.driver.find_element(By.XPATH, xpath_query)
        except StaleElementReferenceException:
            self.driver.implicity_wait(10)
            WebDriverWait(self.driver, wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.XPATH, xpath_query))
            )
            return self.driver.find_element(By.XPATH, xpath_query)
