import pytest

from fenrir.authentication import headless_options
from fenrir.config import FenrirConfig, Authentication, CommonConfig
from fenrir.core_page import webdriver_create, CorePage


def load_config():
    auth = Authentication(
        target_system='indeed',
        username='test@gmail.com',
        password='test',
    )
    common = CommonConfig(
        timeout=10,
        max_retries=3,
        automation_reports_url='https://automation-reports.com',
    )

    return FenrirConfig(
        common=common,
        auth=auth,
    )


@pytest.fixture(scope='class')
def indeed_setup(request):
    config = load_config()
    request.cls.config = config
    driver = webdriver_create('chrome', headless_options())
    request.cls.driver = driver
    core = CorePage(driver, config)
    request.cls.core = core
    yield
    driver.quit()
