import logging

from selenium.webdriver.common.by import By

from fenrir.core_page import CorePage


class LoginObject(CorePage):

    page_url = 'https://www.indeed.com/'

    def __init__(self, driver, config):
        super().__init__(driver, config)
        self.driver = driver
        self.config = config

    def navigate(self):
        self.get(self.page_url)

    def get_signin_button(self):
        return self.find_element(By.CSS_SELECTOR, "div[data-gnav-element-name='SignIn']")

    def login(self):
        self.navigate()
        self.get_signin_button().click()
        self.find_element(By.CSS_SELECTOR, 'input[type="email"]').send_keys(
            self.config.auth.username
        )
        self.find_element(
            By.CSS_SELECTOR, 'button[data-tn-element="auth-page-email-submit-button"]'
        ).click()
        try:
            captcha = self.driver.find_element(
                By.CSS_SELECTOR,
                'div[data-tn-element="auth-page-email-captcha-h-captcha-puzzle-widget"]',
            )
            captcha.click()
        except:
            logging.error("No captcha found")

        logging.info("Moving past captcha")
