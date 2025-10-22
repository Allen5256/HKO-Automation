from __future__ import annotations
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class ForecastPage(BasePage):
    """Page-object for the 9-day forecast screen."""
    BTN_9DAY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("9-day")')
    LIST_DAY_CARDS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*recycler.*|.*list.*|.*forecast.*")')
    ANY_TEXT = (AppiumBy.XPATH, "//*")

    def open_9day_screen(self):
        self.tap(self.BTN_9DAY)

    def get_ninth_day_summary(self):
        items = self.finds(self.LIST_DAY_CARDS)
        if items and len(items) >= 9:
            return (items[8].text or "").strip()
        texts = [el.text for el in self.finds(self.ANY_TEXT) if el.text]
        return "\\n".join(texts[:50])
