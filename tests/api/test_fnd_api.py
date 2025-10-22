from __future__ import annotations
import allure
import pytest
from typing import ContextManager, cast
from utils.date_utils import day_after_tomorrow_hkt, ymd
from validators.fnd_validators import (
    assert_fnd_ok,
    extract_day_after_tomorrow_humidity,
    assert_minimum_contract,
)

@pytest.mark.parametrize("lang", ["en"])
def test_fnd_ok(api_client, lang):
    with cast(ContextManager, allure.step("Send GET to HKO 9-day forecast endpoint")):
        resp = api_client.get_fnd(lang=lang)
    assert_fnd_ok(resp)

def test_extract_day_after_tomorrow_humidity(api_client):
    with cast(ContextManager, allure.step("Get forecast JSON")):
        resp = api_client.get_fnd()
    target_date = ymd(day_after_tomorrow_hkt())
    humidity = extract_day_after_tomorrow_humidity(resp.json(), target_date)
    allure.attach(humidity, name="humidity(day+2)")
    assert humidity and "-" in humidity and humidity.endswith("%"), "Expected range like '60-85%'"
    assert humidity and "-" in humidity and humidity.endswith("%"), "Expected range like '60-85%'"

def test_minimum_contract(api_client):
    resp = api_client.get_fnd()
    assert_minimum_contract(resp.json())
