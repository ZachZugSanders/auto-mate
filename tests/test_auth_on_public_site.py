import pytest
from fenrir import authentication


@pytest.mark.usefixtures('setup')
class TestAuth:

    def test_login(self):
        authentication.auth_headed(self.config, self.element, self.opts)
