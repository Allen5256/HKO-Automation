from __future__ import annotations
import requests

class HKOClient:
    """Thin client for Hong Kong Observatory endpoints used in tests."""
    def __init__(self, base_url, session= None):
        if not base_url:
            raise ValueError("base_url must be provided (from env/config).")
        self.base_url = base_url.rstrip("/")
        self.s = session or requests.Session()
        self.s.headers.update({"Accept": "application/json"})

    def get_fnd(self, lang= "en", timeout= 20):
        """9-day forecast (fnd)"""
        url = f"{self.base_url}/weather.php"
        params = {"dataType": "fnd", "lang": lang}
        return self.s.get(url, params=params, timeout=timeout)
