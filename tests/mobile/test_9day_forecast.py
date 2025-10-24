# tests/mobile/test_9day_forecast.py
import allure


@allure.feature("App UI")
@allure.story("9-day Forecast via Hamburger")
def test_check_9th_day_forecast(home_page, hamburger_menu_page, forecast_9day_page):
    assert home_page.is_loaded(), "Home page did not load"

    with allure.step("Open hamburger menu"):
        home_page.open_hamburger()
        assert hamburger_menu_page.is_open(), "Hamburger drawer did not open"

    with allure.step("Navigate to 9-day Forecast"):
        hamburger_menu_page.go_to_9day_forecast()
        assert forecast_9day_page.is_loaded(), "9-day Forecast page did not load"
        assert forecast_9day_page.has_n_days(9), "Expected at least 9 days in the forecast list"

    with allure.step("Open the 9th day card"):
        forecast_9day_page.open_nth_day(9)
