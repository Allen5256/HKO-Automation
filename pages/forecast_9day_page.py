# pages/forecast_9day_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class Forecast9DayPage(BasePage):
    # Page marker (title/breadcrumb). Replace with a stable id if available.
    TITLE_EN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("9-day Forecast")')
    TITLE_ZH = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("九天")')

    # A card/list item of one day — example: use text pattern or resource-id
    # If the app has ids like item_date / item_rh, replace the locators below.
    LIST_CONTAINER_ID = (AppiumBy.ID, "hko.MyObservatory_v1_0:id/recyclerView")

    def is_loaded(self):
        return self.exists(self.TITLE_EN) or self.exists(self.TITLE_ZH) or self.exists(self.LIST_CONTAINER_ID)

    def open_nth_day(self, n):
        """
        Open the Nth day card (1-based). Scroll if needed.
        """
        # If RecyclerView is present, scroll to position through UiScrollable
        self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().resourceId("hko.MyObservatory_v1_0:id/recyclerView")).scrollToEnd(1)'
        )
        # As a neutral approach, just tap the nth visible item by class (adjust class if different)
        items = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup")
        if not items or len(items) < n:
            raise AssertionError("Not enough day items visible to open the requested day")
        items[n-1].click()
        return True

    def has_n_days(self, expected=9):
        # Lightweight heuristic: count candidate day rows; refine with ids if known
        items = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup")
        return len(items) >= expected
