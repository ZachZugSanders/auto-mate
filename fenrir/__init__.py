import logging
from os import environ

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait

timeout = wait_timeout = 10


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

    match which_driver:
        case 'CHROME':
            from webdriver_manager.chrome import ChromeDriverManager
            return webdriver.Chrome(ChromeDriverManager().install())
        case 'CHROMIUM':
            from webdriver_manager.chrome import ChromeDriverManager
            from webdriver_manager.utils import ChromeType
            return webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        case 'FIREFOX':
            from webdriver_manager.firefox import GeckoDriverManager
            return webdriver.Firefox(executable_path=GeckoDriverManager().install())
        case 'INTERNETEXPLORER':
            logging.warning("Seriously?")
            from webdriver_manager.microsoft import IEDriverManager
            return webdriver.Ie(IEDriverManager().install())
        case 'EDGE':
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            return webdriver.Edge(EdgeChromiumDriverManager().install())
        case 'OPERA':
            from webdriver_manager.opera import OperaDriverManager
            return webdriver.Opera(executable_path=OperaDriverManager().install())
        case 'SAFARI':
            return webdriver.Safari()
        case None:
            logging.error('Specified Driver is not present in webdriver_manager')
            raise NotImplementedError(which_driver)


class CorePage(object):
    """
    Class which will wait for elements to appear. Once the web element has appeared
    operations may be performed upon them.
    """
    def __init__(self, driver):
        self.driver = driver

    def scroll_to_top(self):
        self.driver.execute_script("window.scroll(0, 0);")

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def by_name(self, name_selector):
        try:
            WebDriverWait(self.driver, timeout=wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.NAME, name_selector))
            )
            return self.driver.find_element(By.NAME, name_selector)
        except StaleElementReferenceException:
            self.driver.implicity_wait(10)
            WebDriverWait(self.driver, timeout=wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.NAME, name_selector))
            )
            return self.driver.find_element(By.NAME, name_selector)

    def by_id(self, id_selector):
        try:
            WebDriverWait(self.driver, timeout=wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.ID, id_selector)))
            return self.driver.find_element(By.ID, id_selector)
        except StaleElementReferenceException:
            self.driver.implicity_wait(10)
            WebDriverWait(self.driver, timeout=wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.ID, id_selector)))
            return self.driver.find_element(By.ID, id_selector)

    def by_class_name(self, class_name_selector):
        try:
            WebDriverWait(self.driver, timeout=wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, class_name_selector)))
            return self.driver.find_element(By.CLASS_NAME, class_name_selector)
        except StaleElementReferenceException:
            self.driver.implicity_wait(10)
            WebDriverWait(self.driver, timeout=wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME, class_name_selector)))
            return self.driver.find_element(By.CLASS_NAME, class_name_selector)

    def by_css_selector(self, css_selector):
        try:
            WebDriverWait(self.driver, timeout=wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
            return self.driver.find_element(By.CSS_SELECTOR, css_selector)
        except StaleElementReferenceException:
            self.driver.implicity_wait(10)
            WebDriverWait(self.driver, timeout=wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
            return self.driver.find_element(By.CSS_SELECTOR, css_selector)

    def by_xpath(self, xpath_query):
        try:
            WebDriverWait(self.driver, timeout=wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.XPATH, xpath_query))
            )
            return self.driver.find_element(By.XPATH, xpath_query)
        except StaleElementReferenceException:
            self.driver.implicity_wait(10)
            WebDriverWait(self.driver, timeout=wait_timeout).until(
                expected_conditions.visibility_of_element_located((By.XPATH, xpath_query))
            )
            return self.driver.find_element(By.XPATH, xpath_query)
