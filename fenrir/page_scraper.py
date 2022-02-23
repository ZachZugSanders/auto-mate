import re
from bs4 import BeautifulSoup
from authentication import auth_headless
from auto.fenrir import CorePage
from os import environ


def beautiful_scraper(username, password, cluster, url, html_tag, css_tag, text_to_find):
    driver = auth_headless(username=username, password=password, cluster=cluster)
    driver.get(url=url)
    CorePage(driver).by_id('root')

    # Parse through page source to get the HTML TAG, CSS Selector, and Value.
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    found_items = []
    for i in soup.find_all(html_tag, {css_tag: re.compile(fr'{text_to_find}')}):
        found_items += i
    return found_items
