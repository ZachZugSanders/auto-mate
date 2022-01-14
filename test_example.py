import os
import uuid
from uuid import uuid1
from os import environ

import pytest
from selenium import webdriver

from stuff.authentication import auth_headed
from stuff import CorePage

test_os = os.getenv('TEST_OS')
browser = os.getenv('TEST_BROWSER')
test_name = uuid.uuid4()
test_runner_address = os.getenv('TEST_RUNNER')
username = os.getenv('SITE_USERNAME')
password = os.getenv('SITE_PASSWORD')


@pytest.fixture(scope="class")
def setup_remote_test(request):
    desired_cap = {
        'platform': test_os,
        'browserName': browser,
        'version': "latest",  # this is browser version
        'build': str(uuid1()),
        'name': f'{test_name} - {test_os}: {browser}',
        'screenResolution': "1600x1200",
        'username': environ.get('SAUCE_USERNAME'),
        'accessKey': environ.get('SAUCE_ACCESS_KEY'),
        'extendedDebugging': False,
        'recordScreenshots': True,
        'webdriver.remote.quietExceptions': True
    }
    driver = webdriver.Remote(
            desired_capabilities=desired_cap,
            command_executor=f'{test_runner_address}'
        )

    request.cls.driver = driver
    core = CorePage(driver)
    request.cls.core = core
    driver.maximize_window()
    # Initiate login by going to environment without auth.
    auth_headed(driver=driver, username=username, password=password, site=site)
    driver.get(site)
    yield
    driver.close()
