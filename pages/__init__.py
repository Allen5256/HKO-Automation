from .home_page import HomePage
from .hamburger_menu_page import HamburgerMenuPage
from .forecast_9day_page import Forecast9DayPage

def init_pages(driver):
    # Attach as attributes for convenient dot access in debug/Inspector
    driver.home_page = HomePage(driver)
    driver.hamburger_menu_page = HamburgerMenuPage(driver)
    driver.forecast_9day_page = Forecast9DayPage(driver)