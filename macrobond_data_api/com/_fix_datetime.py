from datetime import datetime, tzinfo
from typing import Optional


def _fix_datetime(time: datetime) -> datetime:
    return datetime(time.year, time.month, time.day, time.hour, time.minute, time.second, time.microsecond, time.tzinfo)


def _fix_datetime_set_tzinfo(time: datetime, local_time_zone: tzinfo) -> datetime:
    time = datetime(time.year, time.month, time.day, time.hour, time.minute, time.second, time.microsecond, time.tzinfo)
    if time.tzinfo is None:
        time = time.replace(tzinfo=local_time_zone)
    return time


def _fix_optional_datetime(time: Optional[datetime]) -> Optional[datetime]:
    return _fix_datetime(time) if time else time
