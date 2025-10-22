from __future__ import annotations
import allure
from utils.allure_helpers import attach_request_response

REQUIRED_KEYS = {"weatherForecast"}  # top-level field used by HKO for 9-day

def assert_fnd_ok(resp):
    """Status + minimal sanity check."""
    try:
        data = resp.json()
    except Exception as e:
        attach_request_response("FND", resp.request.method, resp.url, dict(resp.request.headers), None, resp.status_code, resp.headers, resp.text)
        raise AssertionError(f"Response is not JSON: {e!r}")
    attach_request_response("FND", resp.request.method, resp.url, dict(resp.request.headers), None, resp.status_code, resp.headers, data)
    assert resp.status_code == 200, f"Unexpected status: {resp.status_code}"
    missing = [k for k in REQUIRED_KEYS if k not in data]
    assert not missing, f"Missing keys: {missing}"

def _yyyymmdd(token):
    """Normalize various date formats to YYYYMMDD (string)."""
    if not token:
        return ""
    s = str(token)
    # Keep only digits and take first 8 (YYYYMMDD)
    digits = "".join(ch for ch in s if ch.isdigit())
    return digits[:8] if len(digits) >= 8 else ""

def _extract_humidity_range(item):
    """
    Try multiple shapes:
    - item["rh"] = {"min": 60, "max": 85}
    - item["rhRange"] = "60-85%"
    - item["forecastMinrh"], item["forecastMaxrh"]
    - item["forecastMinrh"]["value"], item["forecastMaxrh"]["value"]
    """
    rh = item.get("rh") or {}
    min_v = rh.get("min")
    max_v = rh.get("max")
    if min_v is not None and max_v is not None:
        return f"{min_v}-{max_v}%"

    rh_range = item.get("rhRange")
    if rh_range:
        return rh_range if str(rh_range).endswith("%") else f"{rh_range}%"

    # Some payloads use forecastMinrh/forecastMaxrh or nested objects
    min_rh = item.get("forecastMinrh")
    max_rh = item.get("forecastMaxrh")
    def _val(x):
        if isinstance(x, dict):
            # common shapes: {"unit":"percent","value":85}
            return x.get("value", x.get("min") or x.get("max"))
        return x
    if min_rh is not None and max_rh is not None:
        a = _val(min_rh)
        b = _val(max_rh)
        if a is not None and b is not None:
            return f"{a}-{b}%"

    return None

def extract_day_after_tomorrow_humidity(fnd_json, target_ymd):
    """
    Return '60-85%' for the target date.
    Robust date matching across 'YYYYMMDD', 'YYYY-MM-DD', 'YYYY-MM-DDTHH:MM:SS+08:00', etc.
    """
    target_key = _yyyymmdd(target_ymd)
    forecasts = fnd_json.get("weatherForecast") or []

    # Try direct match
    for item in forecasts:
        raw_date = item.get("forecastDate") or item.get("forecastDateStr") or item.get("forecastDateFormatted") or ""
        if _yyyymmdd(raw_date) == target_key:
            hr = _extract_humidity_range(item)
            if hr:
                return hr

    # If not found, help debugging: list what dates exist (attach via allure if available)
    available = [_yyyymmdd(i.get("forecastDate") or i.get("forecastDateStr") or i.get("forecastDateFormatted") or "") for i in forecasts]
    try:
        import allure
        allure.attach("\n".join(available), name="available_forecast_dates", attachment_type=allure.attachment_type.TEXT)
    except Exception:
        pass

    raise AssertionError(f"Target date {target_ymd} not found in forecast list; available={available}")

def assert_minimum_contract(fnd_json):
    forecasts = fnd_json.get("weatherForecast") or []
    assert len(forecasts) >= 9, f"Expected at least 9 days, got {len(forecasts)}"
    for i, item in enumerate(forecasts, start=1):
        assert "forecastDate" in item, f"[{i}] missing forecastDate"
        assert "week" in item, f"[{i}] missing week"
        assert "forecastMaxrh" in item or "rh" in item, f"[{i}] missing humidity info"
        assert "forecastMintemp" in item or "forecastMinTemp" in item or "minTemp" in item, f"[{i}] missing min temp"
        assert "forecastMaxtemp" in item or "forecastMaxTemp" in item or "maxTemp" in item, f"[{i}] missing max temp"
