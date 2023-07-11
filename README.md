# Fenrir auto-mate
Generic web UI and API framework that provides examples of what might be
done to test a product.

### Development

This project uses poetry to manage dependencies.
I have generated a requirements.txt from poetry if you want to 
use pip (please don't...)

```pip install poetry```

```poetry install```



---

```python
import pytest

@pytest.mark.usefixtures('setup_fixture')
class TestSuiteOfTests:
    def test_do_some_functionality(self):
        some_stuff = self.core.by_id('placeholder')
        assert some_stuff.text is not ''
```