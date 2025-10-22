import allure
from pages.forecast_page import ForecastPage

@allure.feature("App UI")
@allure.story("9-day Forecast")
def test_check_9th_day_forecast(driver):
    page = ForecastPage(driver)
    with allure.step("Open 9-day Forecast screen"):
        page.open_9day_screen()
    with allure.step("Read the 9th day's card"):
        summary = page.get_ninth_day_summary()
    allure.attach(summary or "(empty)", name="9th_day_summary", attachment_type=allure.attachment_type.TEXT)
    assert summary and len(summary) > 0, "Expected non-empty summary text for the 9th day"
