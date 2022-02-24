# -*- coding: utf-8 -*-

from typing import Optional, Union, overload

from datetime import datetime

from .enums import CalendarDateMode


class StartOrEndPoint():

    def __init__(self, time: str, mode: Optional[CalendarDateMode]) -> None:
        self.time = time
        self.mode = CalendarDateMode.DATA_IN_ANY_SERIES if mode is None else mode

    def __str__(self):
        return self.time + ' mode:' + str(self.mode)

    def __repr__(self):
        return str(self)

    @staticmethod
    def relative_to_observations(
        observations: int, mode: CalendarDateMode = None
    ) -> 'StartOrEndPoint':
        return StartOrEndPoint(str(observations), mode)

    @staticmethod
    def relative_to_years(years: int, mode: CalendarDateMode = None) -> 'StartOrEndPoint':
        return StartOrEndPoint(str(years) + "y", mode)

    @staticmethod
    def relative_to_quarters(quarters: int, mode: CalendarDateMode = None) -> 'StartOrEndPoint':
        return StartOrEndPoint(str(quarters) + "q", mode)

    @staticmethod
    def relative_to_months(months: int, mode: CalendarDateMode = None) -> 'StartOrEndPoint':
        return StartOrEndPoint(str(months) + "m", mode)

    @staticmethod
    def relative_to_weeks(weeks: int, mode: CalendarDateMode = None) -> 'StartOrEndPoint':
        return StartOrEndPoint(str(weeks) + "w", mode)

    @staticmethod
    def relative_to_days(days: int, mode: CalendarDateMode = None) -> 'StartOrEndPoint':
        return StartOrEndPoint(str(days) + "d", mode)

    @overload
    @staticmethod
    def point_in_time(
        yyyy_or_datetime: int,
        mm: int = None,  # pylint: disable = invalid-name
        dd: int = None  # pylint: disable = invalid-name
    ) -> 'StartOrEndPoint':
        ...

    @overload
    @staticmethod
    def point_in_time(
        yyyy_or_datetime: datetime
    ) -> 'StartOrEndPoint':
        ...

    @staticmethod
    def point_in_time(
        yyyy_or_datetime: Union[int, datetime],
        mm: int = None,  # pylint: disable = invalid-name
        dd: int = None  # pylint: disable = invalid-name
    ) -> 'StartOrEndPoint':
        if isinstance(yyyy_or_datetime, datetime):
            return StartOrEndPoint(yyyy_or_datetime.strftime('%Y-%m-%d'), None)
        time = str(yyyy_or_datetime).zfill(4)
        if mm is not None:
            time += '-' + str(mm).zfill(2)
            if dd is not None:
                time += '-' + str(dd).zfill(2)
        return StartOrEndPoint(time, None)

    @staticmethod
    def data_in_any_series() -> 'StartOrEndPoint':
        return StartOrEndPoint('', CalendarDateMode.DATA_IN_ANY_SERIES)

    @staticmethod
    def data_in_all_series() -> 'StartOrEndPoint':
        return StartOrEndPoint('', CalendarDateMode.DATA_IN_ALL_SERIES)
