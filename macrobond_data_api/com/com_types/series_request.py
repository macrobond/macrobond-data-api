# pylint: disable = invalid-name missing-module-docstring
# mypy: disable_error_code = empty-body

from typing import Union, Tuple
from datetime import datetime

from macrobond_data_api.common.enums import CalendarMergeMode, CalendarDateMode

from .series_expression import SeriesExpression


class SeriesRequest:
    """Interface for a Macrobond series request."""

    @property
    def AddedSeries(self) -> Tuple[SeriesExpression]:
        """A list of the added series."""

    @property
    def Frequency(self) -> int:
        """
        The frequency that all series will be converted to.
        The default value is ‘Highest’, which means that all series will be converted to the
        same frequency as the series with the highest frequency.
        """

    @Frequency.setter
    def Frequency(self, new_series_frequency: int) -> None:
        """
        The frequency that all series will be converted to.
        The default value is ‘Highest’, which means that all series will be converted to the
        same frequency as the series with the highest frequency.
        """

    @property
    def CalendarMergeMode(self) -> CalendarMergeMode:
        """
        Determines how to handle points in time that are not available in one or more series.
        The default value is ‘AvailibleInAny’
        """

    @CalendarMergeMode.setter
    def CalendarMergeMode(self, new_calendar_merge_mode: CalendarMergeMode) -> None:
        """
        Determines how to handle points in time that are not available in one or more series.
        The default value is ‘AvailibleInAny’
        """

    @property
    def Weekdays(self) -> int:
        """
        This determines what days of the week that are used when the resulting frequency
        is Daily and the CalendarMergeMode is ‘FullCalendar’.
        """

    @Weekdays.setter
    def Weekdays(self, new_week_days: int) -> None:
        """
        This determines what days of the week that are used when the resulting frequency
        is Daily and the CalendarMergeMode is ‘FullCalendar’.
        """

    @property
    def Currency(self) -> str:
        """
        The currency code based on the three letter IS 4217 codes that will be used to convert
        any series expressed in currency units.
        The default is an empty string, which means that no currency conversion will be done.
        There is a list of the supported currencies on a Currencies List web page.
        """

    @Currency.setter
    def Currency(self, new_currency: str) -> None:
        """
        The currency code based on the three letter IS 4217 codes that will be used to convert
        any series expressed in currency units.
        The default is an empty string, which means that no currency conversion will be done.
        There is a list of the supported currencies on a Currencies List web page.
        """

    @property
    def StartDateMode(self) -> CalendarDateMode:
        """
        Determines if the automatic start of the series is at the first point when there
        is data in any series or the first point where there is data in all series.
        The default is ‘DataInAnySeries’. This setting is not used when the StartDate property
        is set to an absolute point in time.
        """

    @StartDateMode.setter
    def StartDateMode(self, new_start_date_mode: CalendarDateMode) -> None:
        """
        Determines if the automatic start of the series is at the first point when there is
        data in any series or the first point where there is data in all series.
        The default is ‘DataInAnySeries’. This setting is not used when the StartDate
        property is set to an absolute point in time.
        """

    @property
    def StartDate(self) -> Union[None, datetime, str]:
        """
        This specifies the start date used for all the series in the request.
        The value can be empty, a specific date or a string representing a point in time
        as described below.
        If it is empty or a relative reference, the StartDateMode will be used to
        determine the start.
        """

    @StartDate.setter
    def StartDate(self, new_start_date: Union[None, datetime, str]) -> None:
        """
        This specifies the start date used for all the series in the request.
        The value can be empty, a specific date or a string representing a point in time
        as described below.
        If it is empty or a relative reference, the StartDateMode will be used to
        determine the start.
        """

    @property
    def EndDateMode(self) -> CalendarDateMode:
        """
        Determines if the automatic end of the series is at the last point when there
        is data in any series or the last point where there is data in all series.
        The default is ‘DataInAnySeries’.
        This setting is not used when the EndDate property is set to an absolute point in time.
        """

    @EndDateMode.setter
    def EndDateMode(self, new_end_date_mode: CalendarDateMode) -> None:
        """
        Determines if the automatic end of the series is at the last point when there is
        data in any series or the last point where there is data in all series.
        The default is ‘DataInAnySeries’.
        This setting is not used when the EndDate property is set to an absolute point in time.
        """

    @property
    def EndDate(self) -> Union[None, datetime, str]:
        """The end date."""

    @EndDate.setter
    def EndDate(self, new_end_date: Union[None, datetime, str]) -> None:
        """The end date."""

    def AddSeries(self, name: str) -> SeriesExpression:
        """
        Add a series to the list of series to request. You can optionally use the returned
        interface to do further configurations, such as methods for missing
        value and frequency conversion.
        """
