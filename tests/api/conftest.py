import os
import pytest
import requests
from utils.api_client import HKOClient

@pytest.fixture(scope="session")
def api_session():
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    return s

@pytest.fixture(scope="session")
def api_client(api_session):
    base_url = os.getenv("API_BASE_URL", "").strip()
    if not base_url:
        raise RuntimeError("API_BASE_URL is not set. Please configure it in config/api.env")
    return HKOClient(base_url=base_url, session=api_session)
