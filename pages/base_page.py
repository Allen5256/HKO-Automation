# pages/base_page.py
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.timeout = timeout

    def wait_visible(self, locator, timeout=None):
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator, timeout=None):
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(EC.element_to_be_clickable(locator))

    def tap(self, locator, timeout=None):
        el = self.wait_clickable(locator, timeout=timeout)
        el.click()
        return el

    def exists(self, locator, timeout=2):
        end = time.time() + timeout
        while time.time() < end:
            els = self.driver.find_elements(*locator)
            if els:
                return True
            time.sleep(0.2)
        return False

    def current_activity(self):
        try:
            return self.driver.current_activity or ""
        except Exception:
            return ""
