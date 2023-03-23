from datetime import datetime, timezone, timedelta

import pytest

from macrobond_data_api.common.types.format_exception import FormatException
from macrobond_data_api.common.types._parse_iso8601 import _parse_iso8601


def test_parse_iso8601() -> None:
    assert _parse_iso8601("2000") == datetime(2000, 1, 1)
    assert _parse_iso8601("200002") == datetime(2000, 2, 1)
    assert _parse_iso8601("2000-02") == datetime(2000, 2, 1)
    assert _parse_iso8601("20000203") == datetime(2000, 2, 3)
    assert _parse_iso8601("2000-02-03") == datetime(2000, 2, 3)
    assert _parse_iso8601("20000203T04") == datetime(2000, 2, 3, 4)
    assert _parse_iso8601("2000-02-03T04") == datetime(2000, 2, 3, 4)
    assert _parse_iso8601("20000203T0405") == datetime(2000, 2, 3, 4, 5)
    assert _parse_iso8601("2000-02-03T04:05") == datetime(2000, 2, 3, 4, 5)
    assert _parse_iso8601("20000203T040506") == datetime(2000, 2, 3, 4, 5, 6)
    assert _parse_iso8601("2000-02-03T04:05:06") == datetime(2000, 2, 3, 4, 5, 6)
    assert _parse_iso8601("20000203T040506.700") == datetime(2000, 2, 3, 4, 5, 6, 700)
    assert _parse_iso8601("2000-02-03T04:05:06.700") == datetime(2000, 2, 3, 4, 5, 6, 700)
    assert _parse_iso8601("20000203T040506,700") == datetime(2000, 2, 3, 4, 5, 6, 700)
    assert _parse_iso8601("2000-02-03T04:05:06,700") == datetime(2000, 2, 3, 4, 5, 6, 700)
    assert _parse_iso8601("20000203T040506Z") == datetime(2000, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
    assert _parse_iso8601("2000-02-03T04:05:06Z") == datetime(2000, 2, 3, 4, 5, 6, tzinfo=timezone.utc)
    assert _parse_iso8601("20000203T040506+01") == datetime(2000, 2, 3, 4, 5, 6, tzinfo=timezone(timedelta(hours=1)))
    assert _parse_iso8601("2000-02-03T04:05:06+01") == datetime(
        2000, 2, 3, 4, 5, 6, tzinfo=timezone(timedelta(hours=1))
    )
    assert _parse_iso8601("20000203T040506+0130") == datetime(
        2000, 2, 3, 4, 5, 6, tzinfo=timezone(timedelta(hours=1, minutes=30))
    )
    assert _parse_iso8601("2000-02-03T04:05:06+0130") == datetime(
        2000, 2, 3, 4, 5, 6, tzinfo=timezone(timedelta(hours=1, minutes=30))
    )
    assert _parse_iso8601("20000203T040506-01") == datetime(2000, 2, 3, 4, 5, 6, tzinfo=timezone(-timedelta(hours=1)))
    assert _parse_iso8601("2000-02-03T04:05:06-01") == datetime(
        2000, 2, 3, 4, 5, 6, tzinfo=timezone(-timedelta(hours=1))
    )
    assert _parse_iso8601("20000203T040506-0130") == datetime(
        2000, 2, 3, 4, 5, 6, tzinfo=timezone(-timedelta(hours=1, minutes=30))
    )
    assert _parse_iso8601("2000-02-03T04:05:06-01:30") == datetime(
        2000, 2, 3, 4, 5, 6, tzinfo=timezone(-timedelta(hours=1, minutes=30))
    )

    with pytest.raises(FormatException, match="Year is missing or malformatted"):
        _parse_iso8601("abc")
    with pytest.raises(FormatException, match="Year is missing or malformatted"):
        _parse_iso8601("20")
    with pytest.raises(FormatException, match="Year is missing or malformatted"):
        _parse_iso8601("20-01")
    with pytest.raises(FormatException, match="Month is missing or malformatted"):
        _parse_iso8601("2000-1")
    with pytest.raises(FormatException, match="Month is missing or malformatted"):
        _parse_iso8601("2000-")
    with pytest.raises(FormatException, match="Day is missing or malformatted"):
        _parse_iso8601("2000-01-1")
    with pytest.raises(FormatException, match="Day is missing or malformatted"):
        _parse_iso8601("2000-01-")
    with pytest.raises(FormatException, match="Missing - in extended format"):
        _parse_iso8601("2000-0102")
    with pytest.raises(FormatException, match="Missing - in extended format"):
        _parse_iso8601("2000:01:02")

    with pytest.raises(FormatException, match="Hour is missing or malformatted"):
        _parse_iso8601("2000T")
    with pytest.raises(FormatException, match="Hour is missing or malformatted"):
        _parse_iso8601("2000T1")
    with pytest.raises(FormatException, match="Minute is missing or malformatted"):
        _parse_iso8601("2000T01:")
    with pytest.raises(FormatException, match="Minute is missing or malformatted"):
        _parse_iso8601("2000T01:2")
    with pytest.raises(FormatException, match="Second is missing or malformatted"):
        _parse_iso8601("2000T01:02:")
    with pytest.raises(FormatException, match="Second is missing or malformatted"):
        _parse_iso8601("2000T01:02:3")
    with pytest.raises(FormatException, match="Millisecond must be delimited by . or ,"):
        _parse_iso8601("2000T01:02:0304")
    with pytest.raises(FormatException, match="Millisecond is missing or malformatted"):
        _parse_iso8601("2000T01:02:03.")
    with pytest.raises(FormatException, match="Millisecond is missing or malformatted"):
        _parse_iso8601("2000T01:02:03.4")
    with pytest.raises(FormatException, match="Missing : in extended format"):
        _parse_iso8601("2000T01:0203")
    with pytest.raises(FormatException, match="Missing : in extended format"):
        _parse_iso8601("2000T01$02$03")

    with pytest.raises(FormatException, match="Hour is missing or malformatted"):
        _parse_iso8601("2000T01+")
    with pytest.raises(FormatException, match="Hour is missing or malformatted"):
        _parse_iso8601("2000T01+1")
    with pytest.raises(FormatException, match="Minute is missing or malformatted"):
        _parse_iso8601("2000T01+01:")
    with pytest.raises(FormatException, match="Minute is missing or malformatted"):
        _parse_iso8601("2000T01+01:1")
