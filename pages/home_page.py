# pages/home_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class HomePage(BasePage):
    # Hamburger (drawer) button — provide multiple fallbacks
    HAMBURGER_BY_ACC   = (AppiumBy.ACCESSIBILITY_ID, "Open navigation drawer")
    HAMBURGER_BY_DESC  = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Open")')
    HAMBURGER_BY_ID    = (AppiumBy.ID, "hko.MyObservatory_v1_0:id/toolbar")  # adjust if real id exists
    HAMBURGER_BY_CLASS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageButton")')

    # A stable marker on Home page (title, chip, or tab). Replace with a real, stable id if you find one.
    MARKER_EN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Home")')
    MARKER_ZH = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("主頁")')

    def is_loaded(self):
        act = (self.current_activity() or "").lower()
        if "homepage" in act or "home" in act or "main" in act:
            return True
        return self.exists(self.MARKER_EN) or self.exists(self.MARKER_ZH)

    def open_hamburger(self):
        for loc in (self.HAMBURGER_BY_ACC, self.HAMBURGER_BY_DESC, self.HAMBURGER_BY_ID, self.HAMBURGER_BY_CLASS):
            if self.exists(loc):
                self.tap(loc, 8)
                return True
        # Fallback: try the first ImageButton in toolbar area
        self.tap(self.HAMBURGER_BY_CLASS, 8)
        return True
