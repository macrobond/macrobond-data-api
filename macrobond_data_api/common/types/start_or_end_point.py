from typing import Optional, Union, overload

from datetime import datetime

from ..enums import CalendarDateMode


class StartOrEndPoint:
    """
    Defines a start or endpoint of a data intervall. Use this constructor, or one of the static
    methods of this class.

    Parameters
    ----------
    time: str
        - A year, ex. "2010"
        - A year and month, ex. "2010-05"
        - A full date on the format "2010-05-19"
        - A reference relative the end of the interval
            - +/-n, a number of observations, ex. "-10"
            - +/-nd, a number of calendar days, ex. "-30d"
            - +/-nw, a number of weeks, ex. "-7w"
            - +/-nm, a number of months, ex. "-3m"
            - +/-nq, a number of quarters, ex "-2q"
            - +/-ny, a number of years, ex "-5y"

    mode: `macrobond_data_api.common.enums.calendar_date_mode.CalendarDateMode`
        Defines how the automatic start or end is calculated.
    """

    __slots__ = ("time", "mode")

    def __init__(self, time: str, mode: Optional[CalendarDateMode]) -> None:
        self.time = time
        self.mode = CalendarDateMode.DATA_IN_ANY_SERIES if mode is None else mode

    def __repr__(self) -> str:
        return self.time + " mode:" + str(self.mode)

    @staticmethod
    def relative_to_observations(observations: int, mode: CalendarDateMode = None) -> "StartOrEndPoint":
        """
        Create a start or endpoint as a number of observations relative the end of the intervall.
        """
        return StartOrEndPoint(str(observations), mode)

    @staticmethod
    def relative_to_years(years: int, mode: CalendarDateMode = None) -> "StartOrEndPoint":
        """
        Create a start or endpoint as a number of years relative the end of the intervall.
        """
        return StartOrEndPoint(str(years) + "y", mode)

    @staticmethod
    def relative_to_quarters(quarters: int, mode: CalendarDateMode = None) -> "StartOrEndPoint":
        """
        Create a start or endpoint as a number of quarters relative the end of the intervall.
        """
        return StartOrEndPoint(str(quarters) + "q", mode)

    @staticmethod
    def relative_to_months(months: int, mode: CalendarDateMode = None) -> "StartOrEndPoint":
        """
        Create a start or endpoint as a number of months relative the end of the intervall.
        """
        return StartOrEndPoint(str(months) + "m", mode)

    @staticmethod
    def relative_to_weeks(weeks: int, mode: CalendarDateMode = None) -> "StartOrEndPoint":
        """
        Create a start or endpoint as a number of weeks relative the end of the intervall.
        """
        return StartOrEndPoint(str(weeks) + "w", mode)

    @staticmethod
    def relative_to_days(days: int, mode: CalendarDateMode = None) -> "StartOrEndPoint":
        """
        Create a start or endpoint as a number of days relative the end of the intervall.
        """
        return StartOrEndPoint(str(days) + "d", mode)

    @overload
    @staticmethod
    def point_in_time(
        yyyy_or_datetime: int,
        mm: int = None,  # pylint: disable = invalid-name
        dd: int = None,  # pylint: disable = invalid-name
    ) -> "StartOrEndPoint":
        pass

    @overload
    @staticmethod
    def point_in_time(yyyy_or_datetime: datetime) -> "StartOrEndPoint":
        pass

    @staticmethod
    def point_in_time(
        yyyy_or_datetime: Union[int, datetime],
        mm: int = None,  # pylint: disable = invalid-name
        dd: int = None,  # pylint: disable = invalid-name
    ) -> "StartOrEndPoint":
        """
        Create a start or endpoint as a full or partial date.

        Parameters
        ----------
        yyyy_or_datetime: Union[int, datetime]
            A `datetime` or a year. If it is a year, the mm and dd parameters will be used too,
            if specified.
        mm: int
            An optional month 1-12
        dd: int
            An optional day 1-31
        """
        if isinstance(yyyy_or_datetime, datetime):
            return StartOrEndPoint(yyyy_or_datetime.strftime("%Y-%m-%d"), None)
        time = str(yyyy_or_datetime).zfill(4)
        if mm is not None:
            time += "-" + str(mm).zfill(2)
            if dd is not None:
                time += "-" + str(dd).zfill(2)
        return StartOrEndPoint(time, None)

    @staticmethod
    def data_in_any_series() -> "StartOrEndPoint":
        """
        Create a start or endpoint as the first or last point where thers is data in any series.
        """
        return StartOrEndPoint("", CalendarDateMode.DATA_IN_ANY_SERIES)

    @staticmethod
    def data_in_all_series() -> "StartOrEndPoint":
        """
        Create a start or endpoint as the first or last point where thers is data in all series.
        """
        return StartOrEndPoint("", CalendarDateMode.DATA_IN_ALL_SERIES)
