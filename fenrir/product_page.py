import os

from selenium.webdriver.common.by import By

from auto.fenrir import CorePage
import typing


class ProductPage(CorePage):
    """
    /
    """
    BREADCRUMBS = 'nav[aria-label="Breadcrumbs"]'
    IMAGES = ""

    def __init__(self, driver):
        super().__init__(driver)

    def go_to_product_page(self, product_url: str, product_name: str):
        self.driver.get(f"{os.getenv('SITE')}/products/{product_url}")
        self.by_css_selector('body')
        assert product_name in self.driver.title

    def breadcrumbs_on_page(self) -> typing.List:
        breadcrumb = self.by_css_selector(self.BREADCRUMBS)
        crumb_elements = breadcrumb.driver.find_elements("//nav[aria-label='Breadcrumbs']//li//a")
        crumb_list = []
        for crumb in crumb_elements:
            crumb_list.append(crumb.text)
        return crumb_list

    def product_images_section(self):
        self.by_css_selector('div[aria-label="gallery"]')
        return self.driver.find_elements(By.XPATH, "//div[@aria-label='gallery']//img")
    ensure_img_load = """
   "return arguments[0].complete && "+
   "typeof arguments[0].naturalWidth != \"undefined\" && "+
   "arguments[0].naturalWidth > 0", image);

    boolean loaded = false;
    if (result instanceof Boolean) {
      loaded = (Boolean) result;
      System.out.println(loaded);
    """
    # TODO: Can't do anything here because the elements are bare.
    def product_info_section(self):
        product_info_section = self.by_css_selector('')
