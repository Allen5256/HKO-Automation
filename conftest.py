import os
import json
import pytest
import allure
from appium import webdriver
from datetime import datetime
from utils.allure_helpers import attach_kv, attach_json, attach_text, attach_screenshot
from dotenv import load_dotenv
from pathlib import Path



# Attempt to load env from config files if present (optional when not using run_test.ps1)
_CFG = Path(__file__).parent / "config"
for p in [Path.cwd() / "config" / "common.env",
          Path.cwd() / "config" / "ui.env",
          Path.cwd() / "config" / "api.env"]:
    if p.exists():
        load_dotenv(p, override=False)

def _env(name: str, default: str | None = None) -> str | None:

    v = os.environ.get(name, default)
    if v is not None and isinstance(v, str):
        v = v.strip()
    return v


def pytest_addoption(parser):
    parser.addoption("--record-video", action="store_true", default=False, help="(placeholder) record video during mobile tests")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    On failure of test call phase, try attaching a screenshot from the driver fixture.
    """
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv:
            try:
                attach_screenshot(drv, name=f"failed_{item.name}")
            except Exception as e:
                attach_text("screenshot_error.txt", f"Failed to take screenshot: {e!r}")
