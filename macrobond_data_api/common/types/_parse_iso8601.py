from datetime import datetime, timezone, timedelta, date, time
from typing import Optional, Tuple
from .format_exception import FormatException


def _parse_date(s: str) -> Tuple[date, str]:
    if len(s) < 4 or not s[:4].isascii() or not s[:4].isdigit():
        raise FormatException("Year is missing or malformatted")
    year = int(s[:4])
    if len(s) == 4 or s[4] == "T":
        return date(year, 1, 1), s[4:]

    if not s[4].isdigit():
        # extended format, convert to basic
        if s[4] != "-":
            raise FormatException("Missing - in extended format")
        if len(s) >= 9:
            if s[7] != "-":
                raise FormatException("Missing - in extended format")
            s = s[:4] + s[5:7] + s[8:]
        elif len(s) >= 6:
            s = s[:4] + s[5:]

    if len(s) < 6 or not s[4:6].isascii() or not s[4:6].isdigit():
        raise FormatException("Month is missing or malformatted")
    month = int(s[4:6])
    if len(s) == 6 or s[6] == "T":
        return date(year, month, 1), s[6:]

    if len(s) < 8 or not s[6:8].isascii() or not s[6:8].isdigit():
        raise FormatException("Day is missing or malformatted")
    day = int(s[6:8])
    return date(year, month, day), s[8:]


def _parse_timezone(s: str) -> timezone:
    if s[0] == "Z":
        return timezone.utc

    if s[0] != "+" and s[0] != "-":
        raise FormatException("Offset is malformatted")

    direction = 1 if s[0] == "+" else -1
    if len(s) < 3 or not s[1:3].isascii() or not s[1:3].isdigit():
        raise FormatException("Hour is missing or malformatted")
    hour = int(s[1:3])
    if len(s) == 3:
        return timezone(timedelta(hours=hour) * direction)
    if s[3] == ":":
        s = s[:3] + s[4:]

    if len(s) != 5 or not s[3:5].isascii() or not s[3:5].isdigit():
        raise FormatException("Minute is missing or malformatted")
    minute = int(s[3:5])
    return timezone(timedelta(hours=hour, minutes=minute) * direction)


def _parse_time(s: str, tz: Optional[timezone]) -> time:  # pylint: disable=too-many-branches
    if len(s) < 2 or not s[:2].isascii() or not s[:2].isdigit():
        raise FormatException("Hour is missing or malformatted")
    hour = int(s[:2])
    if len(s) == 2:
        return time(hour, 0, 0, tzinfo=tz)

    if not s[2].isdigit():
        # extended format, convert to basic
        if s[2] != ":":
            raise FormatException("Missing : in extended format")
        if len(s) >= 7:
            if s[5] != ":":
                raise FormatException("Missing : in extended format")
            s = s[:2] + s[3:5] + s[6:]
        elif len(s) >= 4:
            s = s[:2] + s[3:]

    if len(s) < 4 or not s[2:4].isascii() or not s[2:4].isdigit():
        raise FormatException("Minute is missing or malformatted")
    minute = int(s[2:4])
    if len(s) == 4:
        return time(hour, minute, 0, tzinfo=tz)

    if len(s) < 6 or not s[4:6].isascii() or not s[4:6].isdigit():
        raise FormatException("Second is missing or malformatted")
    second = int(s[4:6])
    if len(s) == 6:
        return time(hour, minute, second, tzinfo=tz)

    if s[6] not in [".", ","]:
        raise FormatException("Millisecond must be delimited by . or ,")

    if len(s) < 8 or not s[7:].isascii() or not s[7:].isdigit():
        raise FormatException("Millisecond is missing or malformatted")
    exp = 10 ** (6 - (len(s) - 7))
    ms = int(int(s[7:]) * exp)
    return time(hour, minute, second, ms, tzinfo=tz)


def _parse_iso8601(s: str) -> datetime:
    parsed_date, s = _parse_date(s)
    if s and s[0] == "T":
        z = s.find("Z", 1)
        if z == -1:
            z = s.find("+", 1)
        if z == -1:
            z = s.find("-", 1)
        if z != -1:
            tz = _parse_timezone(s[z:])
            parsed_time = _parse_time(s[1:z], tz)
            return datetime.combine(parsed_date, parsed_time)

        parsed_time = _parse_time(s[1:], None)
        return datetime.combine(parsed_date, parsed_time)
    return datetime(parsed_date.year, parsed_date.month, parsed_date.day)
