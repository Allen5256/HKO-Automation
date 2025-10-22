# tests/mobile/conftest.py
import os
import pytest
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options

def _env(name, default=None):
    v = os.getenv(name, default)
    if isinstance(v, str):
        v = v.strip()
    return v

@pytest.fixture(scope="session")
def appium_server_url():
    return _env("APPIUM_SERVER_URL", "http://127.0.0.1:4723")

@pytest.fixture(scope="session")
def android_env():
    # 只存環境值，別預先組 caps，避免混入未加前綴的鍵
    return {
        "PLATFORM_NAME": _env("PLATFORM_NAME", "Android"),
        "AUTOMATION_NAME": _env("AUTOMATION_NAME", "UiAutomator2"),
        "DEVICE_NAME": _env("DEVICE_NAME", "Android Emulator"),
        "APP_PACKAGE": _env("APP_PACKAGE", ""),
        "APP_ACTIVITY": _env("APP_ACTIVITY", "*"),
        "APP_WAIT_ACTIVITY": _env("APP_WAIT_ACTIVITY", "*"),
        "NEW_COMMAND_TIMEOUT": int(_env("NEW_COMMAND_TIMEOUT", "120") or "120"),
    }

@pytest.fixture(scope="function")
def driver(appium_server_url, android_env):
    # 用 Appium Options，全部自己加 vendor 前綴，避免 load_capabilities 自動插入不帶前綴的 automationName
    opts = UiAutomator2Options()
    opts.set_capability("platformName", android_env["PLATFORM_NAME"])              # W3C 允許無前綴
    opts.set_capability("appium:automationName", android_env["AUTOMATION_NAME"])
    opts.set_capability("appium:deviceName", android_env["DEVICE_NAME"])
    opts.set_capability("appium:appPackage", android_env["APP_PACKAGE"])
    opts.set_capability("appium:appActivity", android_env["APP_ACTIVITY"])
    opts.set_capability("appium:appWaitActivity", android_env["APP_WAIT_ACTIVITY"])
    opts.set_capability("appium:newCommandTimeout", android_env["NEW_COMMAND_TIMEOUT"])
    opts.set_capability("appium:autoGrantPermissions", True)
    opts.set_capability("appium:noReset", True)

    drv = webdriver.Remote(appium_server_url, options=opts)
    yield drv
    try:
        drv.quit()
    except Exception:
        pass
