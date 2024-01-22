# Fenrir auto-mate
Generic web UI and API framework that provides examples of what might be
done to test a product.

### Development

This project uses poetry to manage dependencies. To install poetry, run the
following command:

```shell
pip install poetry
```

```shell
poetry install
```

### Framework
- Built to run specific sites which are located in the sites package.
- Uses pytest to run tests.

--- 

```python
import pytest

@pytest.mark.usefixtures('setup_fixture')
class TestSuiteOfTests:
    def test_do_some_functionality(self):
        some_stuff = self.core.by_id('placeholder')
        assert some_stuff.text is not ''
```