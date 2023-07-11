import pytest


@pytest.fixture(scope='class')
def setup(request):
    yield
