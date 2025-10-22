# QA Automation Challenge – MyObservatory (App UI + API)

> **Scope**: Task 1 – App UI automation with Appium + POM; Task 2 – API tests with an API client; unified reporting via Allure.  
> **Language**: Python + Pytest.  
> **Style**: Clean, extensible, consistent with my public repos’ patterns.

---

## 1) Test Case List (preview-friendly table)

### Task 1 – App UI (Android, MyObservatory)
| ID | Title | Precondition | Steps | Expected Results | Notes |
|---|---|---|---|---|---|
| UI-01 | Check the 9th day’s forecast from the 9-day forecast screen | App installed and launches to home | 1. Open app<br>2. Navigate to “9-day Forecast” screen<br>3. Read the 9th item (card)<br>4. Capture displayed summary (e.g., weather icon/desc, min/max temp) | The 9th day’s forecast card is present and readable; fields are non-empty and have valid formats | Resilient selectors with fallbacks |

### Task 2 – API (Hong Kong Observatory 9-day Forecast)
| ID | Title | Endpoint | Steps | Expected Results | Validation Strategy |
|---|---|---|---|---|---|
| API-01 | Request 9-day forecast | `/weather.php?dataType=fnd&lang=en` | 1. Send GET<br>2. Verify status and JSON payload | HTTP 200 and well-formed JSON | keys present (e.g., `weatherForecast`) and types sensible |
| API-02 | Extract “day after tomorrow” humidity | same as API-01 | 1. Compute target date (today+2, HKT)<br>2. Find matching day in payload<br>3. Extract humidity range (e.g., `60-85%`) | Non-empty humidity range string for day after tomorrow | validator parses and returns both min/max as ints; also Allure attaches raw/parsed |
| API-03 | Contract checks (lightweight) | same as API-01 | 1. Verify required keys exist for all 9 entries | All 9 entries contain the minimal required fields | focuses on keys we use (date, humidity, temps, forecastDesc) |

---

## 2) How to Run

### 2.1 Prerequisites
- Python 3.10+
- Java 8+ (for Allure CLI if you want to open HTML reports)
- Node.js 18+ and npm for **local Appium Server** (Appium 2)
- Android SDK / adb on PATH for Android instrumentation
- (Optional) Allure CLI to open HTML reports

### 2.2 Quick Setup
- **Windows (PowerShell)**: `./setup_env.ps1`  
- **macOS / Linux (bash)**: `bash setup_env.sh`

This will create a virtualenv and install project dependencies.

### 2.3 Appium Server (Project-local)
```bash
npm i -g appium
appium driver install uiautomator2
appium
```

### 2.4 Configure via `config/*.env` (no manual exports)
Edit env files instead of exporting variables in your shell:

- `config/ui.env` — UI/Appium capabilities (`PLATFORM_NAME`, `DEVICE_NAME`, `APP_PACKAGE`, `APP_ACTIVITY`, etc)
- `config/api.env` — API base URL (`API_BASE_URL`)

The runner (`run_test.ps1`) will auto-load relevant files based on scope (UI/API).  
Direct `pytest` runs will also auto-load via `python-dotenv`.

> Tip: Discover `appActivity` with `adb shell dumpsys window | grep -i mCurrentFocus` after launching the app.

### 2.5 Run Tests
```powershell
# Preferred (Windows PowerShell): unified runner
.\run_test.ps1 -Scope UI                     # run all UI tests
.\run_test.ps1 -Scope API                    # run all API tests
.\run_test.ps1 -Scope API -Target test_fnd_api.py   # run specific module (via -k)

# Only generate Allure report when tests failed
.\run_test.ps1 -Scope UI -OnlyOnFail
```

**Alternatively (direct pytest, any OS):**
```bash
pytest -n auto --alluredir=allure_results
pytest tests/mobile -n auto --alluredir=allure_results
pytest tests/api -n auto --alluredir=allure_results
```

### 2.6 Open Allure Report
If you use `run_test.ps1`, the report is generated automatically (unless you set `-OnlyOnFail` and tests passed).  
Manual operations:

```bash
allure serve allure_results
# or
allure generate allure_results -o allure_report --clean
```

---

## 3) Design Notes

- **POM**: Shared driver ops (waits, taps, getters) in `BasePage`; screen-specific in `ForecastPage`.
- **API client pattern**: A typed `HKOClient` encapsulates base URL + request wiring; tests remain lean and declarative.
- **Fixtures by scope**: Shared fixtures/hooks in repo-root `conftest.py`; UI-only fixtures in `tests/mobile/conftest.py`; API-only fixtures in `tests/api/conftest.py`.
- **Parametrization**: Use `pytest.mark.parametrize` for variants.
- **Allure utilities**: Central helpers for screenshots, request/response attachments, JSON, and key-value meta.

---

## 4) Project Layout

```
.
├─ pages/
│  ├─ base_page.py
│  ├─ home_page.py
│  ├─ hamburger_menu_page.py
│  └─ forecast_9day_page.py
├─ tests/
│  ├─ mobile/
│  │  ├─ conftest.py
│  │  └─ test_9day_forecast.py
│  └─ api/
│     ├─ conftest.py
│     └─ test_fnd_api.py
├─ validators/
│  └─ fnd_validators.py
├─ utils/
│  ├─ api_client.py
│  ├─ allure_helpers.py
│  └─ date_utils.py
├─ config/
│  ├─ ui.env
│  └─ api.env
├─ conftest.py
└─ README.md
```
