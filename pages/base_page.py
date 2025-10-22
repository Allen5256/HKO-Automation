from __future__ import annotations
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

DEFAULT_TIMEOUT = 20

class BasePage:
    """Base page-object with common methods for all screens."""
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)


    def wait_for_element(self, locator, condition=EC.presence_of_element_located):
        return self.wait.until(condition(locator))

    def tap(self, locator):
        el = None
        try:
            el = self.wait_for_element(locator, condition=EC.element_to_be_clickable)
            el.click()
        except (TimeoutException, ElementClickInterceptedException):
             raise AssertionError(f"Element {locator} not clickable")

    def get_text(self, locator):
        el = self.wait_for_element(locator, condition=EC.presence_of_element_located)
        return el.text

    def find(self, locator):
        return self.driver.find_element(*locator)

    def finds(self, locator):
        return self.driver.find_elements(*locator)
