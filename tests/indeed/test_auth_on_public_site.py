import pytest
from sites.indeed.home_page import LoginObject


@pytest.mark.usefixtures('indeed_setup')
class TestAuth:

    def test_login(self):
        login = LoginObject(self.core, self.config)
        login.login()

