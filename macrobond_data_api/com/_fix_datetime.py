from datetime import datetime
from typing import Optional


def _fix_datetime(time: datetime) -> datetime:
    return datetime(time.year, time.month, time.day, time.hour, time.minute, time.second, time.microsecond, time.tzinfo)


def _fix_optional_datetime(time: Optional[datetime]) -> Optional[datetime]:
    return _fix_datetime(time) if time else time
