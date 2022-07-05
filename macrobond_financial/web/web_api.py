# -*- coding: utf-8 -*-

from datetime import datetime, timezone
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Union,
    Tuple,
    cast,
)

from macrobond_financial.common import Api
from macrobond_financial.common.types import SearchResult, SeriesEntry

from macrobond_financial.common.enums import (
    SeriesWeekdays,
    SeriesFrequency,
    CalendarMergeMode,
)

from macrobond_financial.common.types import (
    MetadataValueInformation,
    MetadataValueInformationItem,
    MetadataAttributeInformation,
    RevisionInfo,
    GetEntitiesError,
    VintageSeries,
    Series,
    Entity,
    SeriesObservationHistory,
    UnifiedSeries,
    UnifiedSerie,
    GetAllVintageSeriesResult,
)

from .session import ProblemDetailsException

if TYPE_CHECKING:  # pragma: no cover
    from .session import Session

    from macrobond_financial.common.types import SearchFilter, StartOrEndPoint

    from .web_types import (
        SearchFilter as WebSearchFilter,
        SearchRequest,
        UnifiedSeriesRequest,
        UnifiedSeriesEntry,
        SeriesWithRevisionsInfoResponse,
        VintageSeriesResponse,
    )

    from .web_types import SeriesResponse, EntityResponse


__pdoc__ = {
    "WebApi.__init__": False,
}


# TODO: @mb-jp impove , can we use a standard lib for this ?
# https://stackoverflow.com/questions/127803/how-do-i-parse-an-iso-8601-formatted-date


def _str_to_datetime_z(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _optional_str_to_datetime_z(datetime_str: Optional[str]) -> Optional[datetime]:
    return _str_to_datetime_z(datetime_str) if datetime_str else None


def _str_to_datetime(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)


def _optional_str_to_datetime(datetime_str: Optional[str]) -> Optional[datetime]:
    return _str_to_datetime(datetime_str) if datetime_str else None


def _create_entity(response: "EntityResponse", name: str) -> Entity:
    error_text = response.get("errorText")

    if error_text:
        return Entity(name, error_text, None)

    return Entity(name, None, cast(Dict[str, Any], response["metadata"]))


def _create_series(response: "SeriesResponse", name: str) -> Series:
    error_text = response.get("errorText")

    if error_text:
        return Series(name, error_text, None, None, None)

    dates = tuple(
        map(
            lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc),
            cast(List[str], response["dates"]),
        )
    )
    values = tuple(
        map(
            lambda x: float(x) if x else None,
            cast(List[Optional[float]], response["values"]),
        )
    )
    # values = cast(Tuple[Optional[float]], response["values"])
    return Series(name, "", cast(Dict[str, Any], response["metadata"]), values, dates)


class WebApi(Api):
    def __init__(self, session: "Session") -> None:
        super().__init__()
        self.__session = session

    @property
    def session(self) -> "Session":
        return self.__session

    # metadata

    def metadata_list_values(self, name: str) -> MetadataValueInformation:
        values = self.session.metadata.list_attribute_values(name)
        return MetadataValueInformation(
            list(
                map(
                    lambda x: MetadataValueInformationItem(
                        name, x["value"], x["description"], x.get("comment")
                    ),
                    values,
                )
            ),
            name,
        )

    def metadata_get_attribute_information(self, *name: str) -> List[MetadataAttributeInformation]:
        def get_metadata_attribute_information(info):
            return MetadataAttributeInformation(
                info["name"],
                info["description"],
                info.get("comment"),
                info["valueType"],
                info["usesValueList"],
                info["canListValues"],
                info["canHaveMultipleValues"],
                info["isDatabaseEntity"],
            )

        info = self.session.metadata.get_attribute_information(*name)
        return list(map(get_metadata_attribute_information, info))

    def metadata_get_value_information(
        self, *name_val: Tuple[str, str]
    ) -> List[MetadataValueInformationItem]:
        ret: List[MetadataValueInformationItem] = []
        try:
            for info in self.session.metadata.get_value_information(*name_val):
                ret.append(
                    MetadataValueInformationItem(
                        info["attributeName"],
                        info["value"],
                        info["description"],
                        info.get("comment"),
                    )
                )
        except ProblemDetailsException as ex:
            if ex.status == 404:
                raise ValueError(ex.detail) from ex
            raise ex
        return ret

    # revision

    def get_revision_info(self, *series_names: str, raise_error: bool = None) -> List[RevisionInfo]:
        def to_obj(name: str, serie: "SeriesWithRevisionsInfoResponse"):
            error_text = serie.get("errorText")
            if error_text:
                return RevisionInfo(
                    name,
                    error_text,
                    False,
                    False,
                    None,
                    None,
                    tuple(),
                )

            time_stamp_of_first_revision = _optional_str_to_datetime_z(
                serie.get("timeStampOfFirstRevision")
            )

            time_stamp_of_last_revision = _optional_str_to_datetime_z(
                serie.get("timeStampOfLastRevision")
            )

            stores_revisions = serie["storesRevisions"]
            if stores_revisions:
                vintage_time_stamps = tuple(
                    map(
                        _str_to_datetime_z,
                        serie["vintageTimeStamps"],
                    )
                )
            else:
                vintage_time_stamps = tuple()

            return RevisionInfo(
                name,
                "",
                stores_revisions,
                serie["hasRevisions"],
                time_stamp_of_first_revision,
                time_stamp_of_last_revision,
                vintage_time_stamps,
            )

        response = self.session.series.get_revision_info(*series_names)

        GetEntitiesError.raise_if(
            self.raise_error if raise_error is None else raise_error,
            map(lambda x, y: (x, y.get("errorText")), series_names, response),
        )

        return list(map(to_obj, series_names, response))

    def get_vintage_series(
        self, time: datetime, *series_names: str, raise_error: bool = None
    ) -> List[VintageSeries]:
        def to_obj(response: "VintageSeriesResponse", series_name: str) -> VintageSeries:
            error_message = response.get("errorText")
            if error_message:
                return VintageSeries(series_name, error_message, None, None, None)

            metadata = cast(Dict[str, Any], response["metadata"])

            revision_time_stamp = cast(str, metadata.get("RevisionTimeStamp"))
            if not revision_time_stamp or time != _str_to_datetime_z(revision_time_stamp):
                raise ValueError("Invalid time")

            values: Tuple[Optional[float], ...] = tuple(
                map(
                    lambda x: float(x) if x else None,
                    cast(List[Optional[float]], response["values"]),
                )
            )

            dates = tuple(map(_str_to_datetime, cast(List[str], response["dates"])))

            return VintageSeries(series_name, None, metadata, values, dates)

        response = self.session.series.fetch_vintage_series(
            time, *series_names, get_times_of_change=False
        )

        series = list(map(to_obj, response, series_names))

        GetEntitiesError.raise_if(
            self.raise_error if raise_error is None else raise_error,
            map(
                lambda x, y: (x, y.error_message if y.is_error else None),
                series_names,
                series,
            ),
        )

        return series

    def get_nth_release(
        self, nth: int, *series_names: str, raise_error: bool = None
    ) -> List[Series]:
        response = self.session.series.fetch_nth_release_series(nth, *series_names)

        series = list(map(_create_series, response, series_names))

        GetEntitiesError.raise_if(
            self.raise_error if raise_error is None else raise_error,
            map(
                lambda x, y: (x, y.error_message if y.is_error else None),
                series_names,
                series,
            ),
        )

        return series

    def get_all_vintage_series(self, series_name: str) -> GetAllVintageSeriesResult:
        try:
            response = self.session.series.fetch_all_vintage_series(series_name)
        except ProblemDetailsException as ex:
            if ex.status == 404:
                raise ValueError("Series not found: " + series_name) from ex
            raise ex

        return GetAllVintageSeriesResult(
            list(map(lambda x: _create_series(x, series_name), response)), series_name
        )

    def get_observation_history(
        self, serie_name: str, *times: datetime
    ) -> List[SeriesObservationHistory]:
        try:
            response = self.session.series.fetch_observation_history(serie_name, list(times))
        except ProblemDetailsException as ex:
            if ex.status == 404:
                raise Exception(ex.detail) from ex
            raise ex

        return list(
            map(
                lambda x: SeriesObservationHistory(
                    _str_to_datetime(x["observationDate"]),
                    tuple(map(lambda v: float(v) if v else None, x["values"])),
                    tuple(map(_optional_str_to_datetime_z, x["timeStamps"])),
                ),
                response,
            )
        )

    # Search

    def entity_search_multi_filter(
        self,
        *filters: "SearchFilter",
        include_discontinued: bool = False,
        no_metadata: bool = False
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
            "noMetadata": no_metadata,
        }

        response = self.__session.search.post_entities(request)

        return SearchResult(response["results"], response.get("isTruncated") is True)

    # Series

    def get_one_series(self, series_name: str, raise_error: bool = None) -> Series:
        return self.get_series(series_name, raise_error=raise_error)[0]

    def get_series(self, *series_names: str, raise_error: bool = None) -> List[Series]:
        response = self.session.series.fetch_series(*series_names)
        series = list(map(_create_series, response, series_names))
        GetEntitiesError.raise_if(
            self.raise_error if raise_error is None else raise_error,
            map(
                lambda x, y: (x, y.error_message if y.is_error else None),
                series_names,
                series,
            ),
        )
        return series

    def get_one_entity(self, entity_name: str, raise_error: bool = None) -> Entity:
        return self.get_entities(entity_name, raise_error=raise_error)[0]

    def get_entities(self, *entity_names: str, raise_error: bool = None) -> List[Entity]:
        response = self.session.series.fetch_entities(*entity_names)
        entitys = list(map(_create_entity, response, entity_names))
        GetEntitiesError.raise_if(
            self.raise_error if raise_error is None else raise_error,
            map(
                lambda x, y: (x, y.error_message if y.is_error else None),
                entity_names,
                entitys,
            ),
        )
        return entitys

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
    ) -> UnifiedSeries:
        def convert_to_unified_series_entry(
            entry_or_name: Union[SeriesEntry, str]
        ) -> "UnifiedSeriesEntry":
            if isinstance(entry_or_name, str):
                entry_or_name = SeriesEntry(entry_or_name)
            entrie = entry_or_name
            return {
                "name": entrie.name,
                "vintage": entrie.vintage.isoformat() if entrie.vintage is not None else None,
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

        response = self.session.series.fetch_unified_series(request)

        str_dates = response.get("dates")
        if str_dates:
            dates = tuple(map(_str_to_datetime, str_dates))
        else:
            dates = tuple()

        series: List[UnifiedSerie] = []
        for i, one_series in enumerate(response["series"]):
            name = request["seriesEntries"][i]["name"]
            error_text = one_series.get("errorText")

            if error_text:
                series.append(UnifiedSerie(name, error_text, {}, tuple()))
            else:
                values = tuple(
                    map(
                        lambda x: float(x) if x else None,
                        cast(List[Optional[float]], one_series["values"]),
                    )
                )
                metadata = cast(Dict[str, Any], one_series["metadata"])
                series.append(UnifiedSerie(name, "", metadata, values))

        ret = UnifiedSeries(series, dates)

        errors = ret.get_errors()
        raise_error = self.raise_error if raise_error is None else raise_error
        if raise_error and len(errors) != 0:
            raise GetEntitiesError(errors)

        return ret
