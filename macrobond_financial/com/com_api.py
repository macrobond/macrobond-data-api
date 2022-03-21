# -*- coding: utf-8 -*-

from typing import List, Union, TYPE_CHECKING

from datetime import datetime

from macrobond_financial.common import Api

from macrobond_financial.common.enums import (
    SeriesWeekdays,
    SeriesFrequency,
    CalendarMergeMode,
)

from macrobond_financial.common.typs import SearchResult, SeriesEntrie

from ._api_return_typs import (
    _ListValuesReturn,
    _GetAttributeInformationReturn,
    _GetRevisionInfoReturn,
    _GetVintageSeriesReturn,
    _GetOneSeriesReturn,
    _GetSeriesReturn,
    _GetOneEntitieReturn,
    _GetEntitiesReturn,
    _GetUnifiedSeriesReturn,
    _fill_metadata_from_entity,
)


if TYPE_CHECKING:  # pragma: no cover
    from macrobond_financial.com.com_typs import Connection

    from macrobond_financial.common.api_return_typs import (
        ListValuesReturn,
        GetAttributeInformationReturn,
        GetRevisionInfoReturn,
        GetVintageSeriesReturn,
        # GetObservationHistoryReturn,
        # GetNthReleaseReturn,
        GetOneSeriesReturn,
        GetSeriesReturn,
        GetOneEntitieReturn,
        GetEntitiesReturn,
        GetUnifiedSeriesReturn,
    )

    from macrobond_financial.common.typs import SearchFilter, StartOrEndPoint

    from .com_typs import Connection, SearchQuery

__pdoc__ = {
    "ComApi.__init__": False,
}


class ComApi(Api):
    def __init__(self, connection: "Connection") -> None:
        super().__init__()
        self.__connection = connection

    @property
    def connection(self) -> "Connection":
        return self.__connection

    # metadata

    def list_values(self, name: str) -> "ListValuesReturn":
        return _ListValuesReturn(self.__connection.Database, name)

    def get_attribute_information(self, name: str) -> "GetAttributeInformationReturn":
        return _GetAttributeInformationReturn(self.__connection.Database, name)

    # revision

    def get_revision_info(
        self, *series_names: str, raise_error: bool = None
    ) -> "GetRevisionInfoReturn":
        return _GetRevisionInfoReturn(
            self.__connection.Database,
            series_names,
            self.raise_error if raise_error is None else raise_error,
        )

    def get_vintage_series(
        self, serie_name: str, time: datetime, raise_error: bool = None
    ) -> "GetVintageSeriesReturn":
        return _GetVintageSeriesReturn(
            self.__connection.Database,
            serie_name,
            time,
            self.raise_error if raise_error is None else raise_error,
        )

    # def get_observation_history(
    #     self, serie_name: str, time: datetime, raise_error: bool = None
    # ) -> "GetObservationHistoryReturn":
    #     return _GetObservationHistoryReturn(
    #         self.__connection.Database,
    #         serie_name,
    #         time,
    #         self.raise_error if raise_error is None else raise_error,
    #     )

    # def get_nth_release(
    #     self, serie_name: str, nth: int, raise_error: bool = None
    # ) -> "GetNthReleaseReturn":
    #     return _GetNthReleaseReturn(
    #         self.__connection.Database,
    #         serie_name,
    #         nth,
    #         self.raise_error if raise_error is None else raise_error,
    #     )

    # Search

    def series_multi_filter(
        self, *filters: "SearchFilter", include_discontinued: bool = False
    ) -> SearchResult:
        querys: List["SearchQuery"] = []
        for _filter in filters:
            query = self.__connection.Database.CreateSearchQuery()

            for entity_type in _filter.entity_types:
                query.SetEntityTypeFilter(entity_type)

            if _filter.text:
                query.Text = _filter.text

            for key in _filter.must_have_values:
                query.AddAttributeValueFilter(key, _filter.must_have_values[key])

            for key in _filter.must_not_have_values:
                query.AddAttributeValueFilter(
                    key, _filter.must_not_have_values[key], False
                )

            for attribute in _filter.must_have_attributes:
                query.AddAttributeFilter(attribute)

            for attribute in _filter.must_not_have_attributes:
                query.AddAttributeFilter(attribute, False)

            query.IncludeDiscontinued = include_discontinued

            querys.append(query)

        result = self.__connection.Database.Search(querys)

        entities = tuple(list(map(_fill_metadata_from_entity, result.Entities)))
        return SearchResult(entities, result.IsTruncated)

    # Search

    def get_one_series(
        self, series_name: str, raise_error: bool = None
    ) -> "GetOneSeriesReturn":
        return _GetOneSeriesReturn(
            self.__connection.Database,
            series_name,
            self.raise_error if raise_error is None else raise_error,
        )

    def get_series(
        self, *series_names: str, raise_error: bool = None
    ) -> "GetSeriesReturn":
        return _GetSeriesReturn(
            self.__connection.Database,
            series_names,
            self.raise_error if raise_error is None else raise_error,
        )

    def get_one_entitie(
        self, entity_name: str, raise_error: bool = None
    ) -> "GetOneEntitieReturn":
        return _GetOneEntitieReturn(
            self.__connection.Database,
            entity_name,
            self.raise_error if raise_error is None else raise_error,
        )

    def get_entities(
        self, *entity_names: str, raise_error: bool = None
    ) -> "GetEntitiesReturn":
        return _GetEntitiesReturn(
            self.__connection.Database,
            entity_names,
            self.raise_error if raise_error is None else raise_error,
        )

    def get_unified_series(
        self,
        *series_entries: Union[SeriesEntrie, str],
        frequency=SeriesFrequency.HIGHEST,
        weekdays: SeriesWeekdays = SeriesWeekdays.FULL_WEEK,
        calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ANY,
        currency="",
        start_point: "StartOrEndPoint" = None,
        end_point: "StartOrEndPoint" = None,
        raise_error: bool = None
    ) -> "GetUnifiedSeriesReturn":
        request = self.__connection.Database.CreateUnifiedSeriesRequest()
        for entrie_or_name in series_entries:
            if isinstance(entrie_or_name, str):
                entrie_or_name = SeriesEntrie(entrie_or_name)

            entrie = entrie_or_name
            series_expression = request.AddSeries(entrie.name)

            series_expression.MissingValueMethod = entrie.missing_value_method

            series_expression.ToLowerFrequencyMethod = entrie.to_lowerfrequency_method

            series_expression.ToHigherFrequencyMethod = (
                entrie_or_name.to_higherfrequency_method
            )

            series_expression.PartialPeriodsMethod = (
                entrie_or_name.partial_periods_method
            )

        request.Frequency = frequency

        request.Weekdays = weekdays

        request.CalendarMergeMode = calendar_merge_mode

        request.Currency = currency

        if start_point:
            request.StartDate = start_point.time
            request.StartDateMode = start_point.mode

        if end_point:
            request.EndDate = end_point.time
            request.EndDateMode = end_point.mode

        return _GetUnifiedSeriesReturn(
            self.__connection.Database,
            request,
            self.raise_error if raise_error is None else raise_error,
        )
