# Auto-mate
Generic web UI and API framework that provides examples of what might be
done to test a product.

---

```python
import stuff
import pytest


@pytest.mark.usefixtures('setup_remote_test')
class TestSomeStuff:
    def test_do_some_stuff(self):
        some_stuff = self.core.by_id('placeholder')
        assert some_stuff.text is not ''
```