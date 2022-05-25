# -*- coding: utf-8 -*-

from datetime import datetime
from typing import TYPE_CHECKING, Sequence, Union, Tuple

from macrobond_financial.common import Api
from macrobond_financial.common.types import SearchResult, SeriesEntry

from macrobond_financial.common.enums import (
    SeriesWeekdays,
    SeriesFrequency,
    CalendarMergeMode,
)

from ._api_return_typs import (
    _GetAttributeInformationReturn,
    _ListValuesReturn,
    _GetRevisionInfoReturn,
    _GetVintageSeriesReturn,
    _GetNthReleaseReturn,
    _GetOneSeriesReturn,
    _GetSeriesReturn,
    _GetOneEntityReturn,
    _GetEntitiesReturn,
    _GetUnifiedSeriesReturn,
    _GetValueInformationReturn,
    _GetObservationHistoryReturn,
)

if TYPE_CHECKING:  # pragma: no cover
    from .session import Session

    from macrobond_financial.common.api_return_types import (
        ListValuesReturn,
        GetAttributeInformationReturn,
        GetRevisionInfoReturn,
        GetVintageSeriesReturn,
        GetObservationHistoryReturn,
        GetNthReleaseReturn,
        GetOneSeriesReturn,
        GetSeriesReturn,
        GetOneEntityReturn,
        GetEntitiesReturn,
        GetUnifiedSeriesReturn,
        GetValueInformationReturn,
    )

    from macrobond_financial.common.types import SearchFilter, StartOrEndPoint

    from .web_types import (
        SearchFilter as WebSearchFilter,
        SearchRequest,
        UnifiedSeriesRequest,
        UnifiedSeriesEntry,
    )


__pdoc__ = {
    "WebApi.__init__": False,
}


class WebApi(Api):
    @property
    def session(self) -> "Session":
        return self.__session

    def __init__(self, session: "Session") -> None:
        super().__init__()
        self.__session = session

    # metadata

    def metadata_list_values(self, name: str) -> "ListValuesReturn":
        return _ListValuesReturn(self.__session, name)

    def metadata_get_attribute_information(
        self, name: str
    ) -> "GetAttributeInformationReturn":
        return _GetAttributeInformationReturn(self.__session, name)

    def metadata_get_value_information(
        self, *name_val: Tuple[str, str]
    ) -> "GetValueInformationReturn":
        return _GetValueInformationReturn(self.__session, name_val)

    # revision

    def get_revision_info(
        self, *series_names: str, raise_error: bool = None
    ) -> "GetRevisionInfoReturn":
        return _GetRevisionInfoReturn(
            self.__session,
            series_names,
            self.raise_error if raise_error is None else raise_error,
        )

    def get_vintage_series(
        self, serie_name: str, time: datetime, raise_error: bool = None
    ) -> "GetVintageSeriesReturn":
        return _GetVintageSeriesReturn(
            self.__session,
            serie_name,
            time,
            self.raise_error if raise_error is None else raise_error,
        )

    def get_observation_history(
        self, serie_name: str, times: Sequence[datetime]
    ) -> "GetObservationHistoryReturn":
        return _GetObservationHistoryReturn(
            self.__session,
            serie_name,
            times,
        )

    def get_nth_release(
        self, serie_name: str, nth: int, raise_error: bool = None
    ) -> "GetNthReleaseReturn":
        return _GetNthReleaseReturn(
            self.__session,
            serie_name,
            nth,
            self.raise_error if raise_error is None else raise_error,
        )

    # Search

    def entity_search_multi_filter(
        self, *filters: "SearchFilter", include_discontinued: bool = False
    ) -> SearchResult:
        def convert_filter_to_web_filter(_filter: "SearchFilter") -> "WebSearchFilter":
            return {
                "text": _filter.text,
                "entityTypes": list(_filter.entity_types),
                "mustHaveValues": _filter.must_have_values,
                "mustNotHaveValues": _filter.must_not_have_values,
                "mustHaveAttributes": list(_filter.must_have_attributes),
                "mustNotHaveAttributes": list(_filter.must_not_have_attributes),
            }

        web_filters = list(map(convert_filter_to_web_filter, filters))

        request: "SearchRequest" = {
            "filters": web_filters,
            "includeDiscontinued": include_discontinued,
        }

        response = self.__session.search.post_entities(request)

        return SearchResult(
            tuple(response["results"]), response.get("isTruncated") is True
        )

    # Series

    def get_one_series(
        self, series_name: str, raise_error: bool = None
    ) -> "GetOneSeriesReturn":
        return _GetOneSeriesReturn(
            self.__session,
            series_name,
            self.raise_error if raise_error is None else raise_error,
        )

    def get_series(
        self, *series_names: str, raise_error: bool = None
    ) -> "GetSeriesReturn":
        return _GetSeriesReturn(
            self.__session,
            series_names,
            self.raise_error if raise_error is None else raise_error,
        )

    def get_one_entity(
        self, entity_name: str, raise_error: bool = None
    ) -> "GetOneEntityReturn":
        return _GetOneEntityReturn(
            self.__session,
            entity_name,
            self.raise_error if raise_error is None else raise_error,
        )

    def get_entities(
        self, *entity_names: str, raise_error: bool = None
    ) -> "GetEntitiesReturn":
        return _GetEntitiesReturn(
            self.__session,
            entity_names,
            self.raise_error if raise_error is None else raise_error,
        )

    def get_unified_series(
        self,
        *series_entries: Union[SeriesEntry, str],
        frequency=SeriesFrequency.HIGHEST,
        weekdays: SeriesWeekdays = SeriesWeekdays.FULL_WEEK,
        calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ANY,
        currency="",
        start_point: "StartOrEndPoint" = None,
        end_point: "StartOrEndPoint" = None,
        raise_error: bool = None
    ) -> "GetUnifiedSeriesReturn":
        def convert_to_unified_series_entry(
            entry_or_name: Union[SeriesEntry, str]
        ) -> "UnifiedSeriesEntry":
            if isinstance(entry_or_name, str):
                entry_or_name = SeriesEntry(entry_or_name)
            entrie = entry_or_name
            return {
                "name": entrie.name,
                "missingValueMethod": entrie.missing_value_method,
                "partialPeriodsMethod": entrie.partial_periods_method,
                "toLowerFrequencyMethod": entrie.to_lowerfrequency_method,
                "toHigherFrequencyMethod": entrie.to_higherfrequency_method,
            }

        web_series_entries = list(map(convert_to_unified_series_entry, series_entries))

        request: "UnifiedSeriesRequest" = {
            "frequency": frequency,
            "weekdays": weekdays,
            "calendarMergeMode": calendar_merge_mode,
            "currency": currency,
            "seriesEntries": web_series_entries,
        }

        if start_point:
            request["startPoint"] = start_point.time
            request["startDateMode"] = start_point.mode

        if end_point:
            request["endPoint"] = end_point.time
            request["endDateMode"] = end_point.mode

        return _GetUnifiedSeriesReturn(
            self.__session,
            request,
            self.raise_error if raise_error is None else raise_error,
        )
