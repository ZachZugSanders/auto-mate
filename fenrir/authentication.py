import os
import logging
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from fenrir.config import FenrirConfig
from fenrir.core_page import CorePage, webdriver_create


def headless_options():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')


@dataclass
class LoginElements:
    username_input: str
    password_input: str
    login_button: str


def get_auth_cookies(config: FenrirConfig, elements: LoginElements) -> List[Dict]:
    """
    This method does a login for 3 leg authentication and returns the cookies which
    can then be used later for tests.
    """
    driver = webdriver_create(browser='chrome', opts=headless_options())
    core = CorePage(driver, config)
    core.get(config.auth.target_system)
    core.find_element(By.ID, elements.username_input).send_keys(config.auth.username)
    core.find_element(By.ID, elements.password_input).send_keys(config.auth.password)
    core.find_element(By.ID, elements.login_button).click()
    cookies = driver.get_cookies()
    driver.quit()
    return cookies

def generate_token_file(cookies: List[Dict]):
    """
    Creates a file that stores the oauth2 token required to access clusters.
    :return: Name of file.
    """
    _filename = f"{os.getcwd()}/authentication_file.json"
    auth_file_path = Path(_filename)
    # TODO: Parse the cookies
    auth_cookie = cookies[0]
    if auth_file_path.is_file():
        logging.info(auth_file_path)
        return auth_file_path
    else:
        with open(_filename, 'w') as f:
            f.write(json.dumps(auth_cookie))
        return _filename
