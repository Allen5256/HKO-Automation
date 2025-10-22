from __future__ import annotations
from datetime import datetime, timedelta, timezone

# Hong Kong is UTC+8 without DST
HKT = timezone(timedelta(hours=8))

def today_hkt():
    return datetime.now(tz=HKT)

def day_after_tomorrow_hkt():
    return today_hkt().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=2)

def ymd(dt):
    return dt.strftime("%Y-%m-%d")
