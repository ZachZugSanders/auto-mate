import os
import time
import logging
import json
from pathlib import Path
from os import environ

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from auto.fenrir import CorePage


class LoginPage:
    login_url = os.getenv('LOGIN_SITE')
    input_login_username_id = os.getenv('LOGIN_USERNAME')
    input_login_password_id = os.getenv('LOGIN_PASSWORD')
    button_login_sign_in_id = os.getenv('LOGIN_BUTTON')


def auth_headless(username: str, password: str, cluster: str):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    driver.get(cluster)
    core = CorePage(driver=driver)
    core.by_id(LoginPage.input_login_username_id).send_keys(username)
    pw = core.by_id(LoginPage.input_login_password_id)
    pw.send_keys(password)
    pw.send_keys(Keys.RETURN)
    waiting = 0
    timeout = 20
    while waiting <= timeout:
        if driver.current_url.__contains__(cluster):
            break
        else:
            time.sleep(1)
        waiting += 1
    cookies = driver.get_cookies()
    logging.info(cookies)
    driver.quit()
    return cookies[0]


def auth_headed(driver, username: str, password: str, site: str):
    core = CorePage(driver)
    driver.get(site)
    core.by_id(LoginPage.input_login_username_id).send_keys(username)
    core.by_id(LoginPage.input_login_password_id).send_keys(password)
    core.by_id(LoginPage.button_login_sign_in_id).click()
    waiting = 0
    timeout = 20
    while waiting <= timeout:
        if driver.current_url.__contains__(site):
            break
        else:
            time.sleep(1)
        waiting += 1


FILENAME = "../../tests/api/authentication_file.json"
USERNAME = environ.get('SITE_USERNAME')
PASSWORD = environ.get('SITE_PASSWORD')
SITE = environ.get('SITE')

assert USERNAME
assert PASSWORD
assert SITE


def get_auth_token(username: str, password: str, site: str):
    token = auth_headless(username=username, password=password, cluster=site)
    cookie = token['value']
    environ['AUTH_TOKEN_VALUE'] = cookie
    environ['AUTH_TOKEN_NAME'] = '_oauth2_proxy'
    return {environ.get('AUTH_TOKEN_NAME'): environ.get('AUTH_TOKEN_VALUE')}


def token_file():
    """
    Creates a file that stores the oauth2 token required to access clusters.
    :return: Name of file.
    """
    auth_file_path = Path(FILENAME)
    if auth_file_path.is_file():
        logging.info(auth_file_path)
        return auth_file_path
    else:
        _oauth_proxy_cookie = get_auth_token(username=USERNAME, password=PASSWORD, site=SITE)
        with open(FILENAME, 'w') as f:
            f.write(json.dumps(_oauth_proxy_cookie))
        return FILENAME
