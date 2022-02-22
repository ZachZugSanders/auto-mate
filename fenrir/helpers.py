from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep


def clear_element(element):
    element.send_keys(Keys.COMMAND + 'a')
    element.send_keys(Keys.BACKSPACE)


def element_text_is_not_empty(driver, css_element, timeout=10):
    """
    Function to try to combat race condition where an element would
    load before it actually had useful data.
    :param timeout: in seconds
    :param driver:  is the web driver instance
    :param css_element:  is the element and is only founding using CSS selector
    """
    not_supposed_to_be_empty = WebDriverWait(driver, 30).until(
        lambda d: d.find_element_by_css_selector(css_element).text)
    i = 0
    while i < timeout:
        if not_supposed_to_be_empty == '':
            i += 1
            # Screams internally
            sleep(1)
        else:
            not_supposed_to_be_empty = WebDriverWait(driver, 30).until(
                lambda d: d.find_element_by_css_selector(css_element).text)
    return not_supposed_to_be_empty
