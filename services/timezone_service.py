from zoneinfo import ZoneInfo
from datetime import timezone, datetime

KYIV_TZ = ZoneInfo("Europe/Kyiv")

def to_local(dt: datetime) -> datetime:
    dt = dt.replace(tzinfo=timezone.utc)
    dt = dt.astimezone(KYIV_TZ)
    return dt