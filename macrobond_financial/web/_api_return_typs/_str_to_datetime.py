# -*- coding: utf-8 -*-

from typing import Optional

from datetime import datetime, timezone


def _str_to_datetime_z(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc
    )


def _optional_str_to_datetime_z(datetime_str: Optional[str]) -> Optional[datetime]:
    return _str_to_datetime_z(datetime_str) if datetime_str else None


def _str_to_datetime(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S").replace(
        tzinfo=timezone.utc
    )


def _optional_str_to_datetime(datetime_str: Optional[str]) -> Optional[datetime]:
    return _str_to_datetime(datetime_str) if datetime_str else None
