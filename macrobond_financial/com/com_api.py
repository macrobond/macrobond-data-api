# -*- coding: utf-8 -*-

from math import isnan
from typing import Any, Dict, List, Tuple, Union, TYPE_CHECKING, cast, Sequence

from datetime import datetime, timezone

from macrobond_financial.common import Api

from macrobond_financial.common.enums import (
    SeriesWeekdays,
    SeriesFrequency,
    CalendarMergeMode,
)

from macrobond_financial.common.types import (
    SearchResult,
    SeriesEntry,
    MetadataValueInformation,
    MetadataValueInformationItem,
    MetadataAttributeInformation,
    RevisionInfo,
    GetEntitiesError,
    VintageSeries,
    Series,
    Entity,
    UnifiedSerie,
    UnifiedSeries,
    GetAllVintageSeriesResult,
    SeriesObservationHistory,
)

if TYPE_CHECKING:  # pragma: no cover
    from macrobond_financial.com.com_types import Connection

    from macrobond_financial.common.enums import MetadataAttributeType

    from macrobond_financial.common.types import SearchFilter, StartOrEndPoint

    from .com_types import Connection, SearchQuery, Database, SeriesWithRevisions

    from .com_types import Series as ComSeries, Entity as ComEntity

__pdoc__ = {
    "ComApi.__init__": False,
}


def _fill_metadata_from_entity(com_entity: "ComEntity") -> Dict[str, Any]:
    ret = {}
    metadata = com_entity.Metadata

    for names_and_description in metadata.ListNames():
        name = names_and_description[0]
        values = metadata.GetValues(name)
        ret[name] = values[0] if len(values) == 1 else list(values)

    if "FullDescription" not in ret:
        ret["FullDescription"] = com_entity.Title

    return ret


def _datetime_to_datetime(dates: Sequence[datetime]) -> Tuple[datetime, ...]:
    return tuple(
        map(
            lambda x: datetime(
                x.year,
                x.month,
                x.day,
                x.hour,
                x.minute,
                x.second,
                x.microsecond,
                timezone.utc,
            ),
            dates,
        )
    )


def _create_entity(com_entity: "ComEntity", name: str) -> Entity:
    if com_entity.IsError:
        return Entity(name, com_entity.ErrorMessage, None)
    return Entity(name, None, _fill_metadata_from_entity(com_entity))


def _create_series(com_series: "ComSeries", name: str) -> Series:
    if com_series.IsError:
        return Series(name, com_series.ErrorMessage, None, None, None)
    return Series(
        name,
        None,
        _fill_metadata_from_entity(com_series),
        com_series.Values,
        _datetime_to_datetime(com_series.DatesAtStartOfPeriod),
    )


class ComApi(Api):
    def __init__(self, connection: "Connection") -> None:
        super().__init__()
        self.__connection = connection

    @property
    def connection(self) -> "Connection":
        return self.__connection

    @property
    def database(self) -> "Database":
        return self.__connection.Database

    # metadata

    def metadata_list_values(self, name: str) -> MetadataValueInformation:
        info = self.database.GetMetadataInformation(name)
        values = info.ListAllValues()

        return MetadataValueInformation(
            list(
                map(
                    lambda x: MetadataValueInformationItem(name, x.Value, x.Description, x.Comment),
                    values,
                )
            ),
            name,
        )

    def metadata_get_attribute_information(self, *names: str) -> List[MetadataAttributeInformation]:
        def get_metadata_attribute_information(name: str):
            info = self.database.GetMetadataInformation(name)
            return MetadataAttributeInformation(
                info.Name,
                info.Description,
                info.Comment,
                cast("MetadataAttributeType", info.ValueType),
                info.UsesValueList,
                info.CanListValues,
                info.CanHaveMultipleValues,
                info.IsDatabaseEntity,
            )

        return list(map(get_metadata_attribute_information, names))

    def metadata_get_value_information(
        self, *name_val: Tuple[str, str]
    ) -> List[MetadataValueInformationItem]:
        def is_error_with_text(ex: Exception, text: str) -> bool:
            return len(ex.args) >= 3 and len(ex.args[2]) >= 3 and ex.args[2][2].startswith(text)

        ret: List[MetadataValueInformationItem] = []
        for i in name_val:
            name = i[0]
            val = i[1]

            try:
                info = self.database.GetMetadataInformation(name)
            except Exception as ex:
                if is_error_with_text(ex, "Unknown metadata name: "):
                    raise ValueError("Unknown attribute: " + name) from ex
                raise ex

            try:
                value_info = info.GetValueInformation(val)
            except Exception as ex:
                if is_error_with_text(
                    ex, "The attribute '" + name + "' does not have a value called "
                ):
                    raise ValueError("Unknown attribute value: " + name + "," + val) from ex
                raise ex

            ret.append(
                MetadataValueInformationItem(
                    name, value_info.Value, value_info.Description, value_info.Comment
                )
            )
        return ret

    # revision

    def get_revision_info(self, *series_names: str, raise_error: bool = None) -> List[RevisionInfo]:
        def to_obj(name: str, serie: "SeriesWithRevisions"):
            if serie.IsError:
                return RevisionInfo(
                    name,
                    serie.ErrorMessage,
                    False,
                    False,
                    None,
                    None,
                    tuple(),
                )

            vintage_time_stamps = _datetime_to_datetime(serie.GetVintageDates())

            time_stamp_of_first_revision = vintage_time_stamps[0] if serie.HasRevisions else None
            time_stamp_of_last_revision = vintage_time_stamps[-1] if serie.HasRevisions else None

            return RevisionInfo(
                name,
                "",
                serie.StoresRevisions,
                serie.HasRevisions,
                time_stamp_of_first_revision,
                time_stamp_of_last_revision,
                vintage_time_stamps,
            )

        series = self.database.FetchSeriesWithRevisions(series_names)

        GetEntitiesError.raise_if(
            self.raise_error if raise_error is None else raise_error,
            map(
                lambda x, y: (x, y.ErrorMessage if y.IsError else None),
                series_names,
                series,
            ),
        )

        return list(map(to_obj, series_names, series))

    def get_vintage_series(
        self, time: datetime, *series_names: str, raise_error: bool = None
    ) -> List[VintageSeries]:
        def to_obj(series_name: str) -> VintageSeries:
            series_with_revisions = self.database.FetchOneSeriesWithRevisions(series_name)

            if series_with_revisions.IsError:
                return VintageSeries(
                    series_name,
                    series_with_revisions.ErrorMessage,
                    None,
                    None,
                    None,
                )

            try:
                series = series_with_revisions.GetVintage(time)
            except OSError as os_error:
                if os_error.errno == 22 and os_error.strerror == "Invalid argument":
                    raise ValueError("Invalid time") from os_error
                raise os_error

            if series.IsError:
                return VintageSeries(
                    series_name,
                    series.ErrorMessage,
                    None,
                    None,
                    None,
                )

            series_values = series.Values

            padding_front = 0
            for value in series_values:
                if value is None or not isnan(value):
                    break
                padding_front = padding_front + 1

            padding_back = 0
            for value in series_values[::-1]:
                if value is None or not isnan(value):
                    break
                padding_back = padding_back + 1

            padding_back = len(series_values) - padding_back

            values = tuple(series_values[padding_front:padding_back])

            dates = _datetime_to_datetime(series.DatesAtStartOfPeriod[padding_front:padding_back])

            return VintageSeries(
                series_name,
                "",
                _fill_metadata_from_entity(series),
                values,
                dates,
            )

        series = list(map(to_obj, series_names))

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
        def to_obj(series_name: str) -> Series:
            series_with_revisions = self.database.FetchOneSeriesWithRevisions(series_name)

            if series_with_revisions.IsError:
                return Series(
                    series_name,
                    series_with_revisions.ErrorMessage,
                    None,
                    None,
                    None,
                )

            series = series_with_revisions.GetNthRelease(nth)
            if series.IsError:
                return Series(
                    series_name,
                    series.ErrorMessage,
                    None,
                    None,
                    None,
                )

            values = tuple(map(lambda x: None if isnan(x) else x, series.Values))  # type: ignore

            dates = _datetime_to_datetime(series.DatesAtStartOfPeriod)

            return Series(
                series_name,
                None,
                _fill_metadata_from_entity(series),
                values,
                dates,
            )

        series = list(map(to_obj, series_names))

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
        series_with_revisions = self.database.FetchOneSeriesWithRevisions(series_name)

        if series_with_revisions.IsError:
            if series_with_revisions.ErrorMessage == "Not found":
                raise ValueError("Series not found: " + series_name)
            raise Exception(series_with_revisions.ErrorMessage)

        return GetAllVintageSeriesResult(
            list(
                map(
                    lambda x: _create_series(x, series_name),
                    series_with_revisions.GetCompleteHistory(),
                )
            ),
            series_name,
        )

    def get_observation_history(
        self, serie_name: str, *times: datetime
    ) -> List[SeriesObservationHistory]:

        series_with_revisions = self.database.FetchOneSeriesWithRevisions(serie_name)

        if series_with_revisions.IsError:
            if series_with_revisions.ErrorMessage == "Not found":
                raise ValueError("Not found " + serie_name)
            raise Exception(series_with_revisions.ErrorMessage)

        def to_obj(time: datetime) -> SeriesObservationHistory:
            series = series_with_revisions.GetObservationHistory(time)
            dates = _datetime_to_datetime(series.DatesAtStartOfPeriod)
            return SeriesObservationHistory(time, series.Values, dates)

        return list(map(to_obj, times))

    # Search

    def entity_search_multi_filter(
        self,
        *filters: "SearchFilter",
        include_discontinued: bool = False,
        no_metadata: bool = False  # pylint: disable=unused-argument
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
                query.AddAttributeValueFilter(key, _filter.must_not_have_values[key], False)

            for attribute in _filter.must_have_attributes:
                query.AddAttributeFilter(attribute)

            for attribute in _filter.must_not_have_attributes:
                query.AddAttributeFilter(attribute, False)

            query.IncludeDiscontinued = include_discontinued

            querys.append(query)

        result = self.__connection.Database.Search(querys)

        entities = list(map(_fill_metadata_from_entity, result.Entities))
        return SearchResult(entities, result.IsTruncated)

    # Series

    def get_one_series(self, series_name: str, raise_error: bool = None) -> Series:
        return self.get_series(series_name, raise_error=raise_error)[0]

    def get_series(self, *series_names: str, raise_error: bool = None) -> List[Series]:
        com_series = self.database.FetchSeries(series_names)
        series = list(map(_create_series, com_series, series_names))
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
        com_entitys = self.database.FetchEntities(entity_names)
        entitys = list(map(_create_entity, com_entitys, entity_names))
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
        request = self.__connection.Database.CreateUnifiedSeriesRequest()
        for entry_or_name in series_entries:
            if isinstance(entry_or_name, str):
                entry_or_name = SeriesEntry(entry_or_name)

            entrie = entry_or_name
            series_expression = request.AddSeries(entrie.name)

            series_expression.MissingValueMethod = entrie.missing_value_method

            series_expression.ToLowerFrequencyMethod = entrie.to_lowerfrequency_method

            series_expression.ToHigherFrequencyMethod = entry_or_name.to_higherfrequency_method

            series_expression.PartialPeriodsMethod = entry_or_name.partial_periods_method

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

        com_series = self.database.FetchSeries(request)

        first = next(filter(lambda x: not x.IsError, com_series), None)
        if first:
            dates = _datetime_to_datetime(first.DatesAtStartOfPeriod)
        else:
            dates = tuple()

        series: List[UnifiedSerie] = []

        for i, com_one_series in enumerate(com_series):
            name = request.AddedSeries[i].Name
            if com_one_series.IsError:
                series.append(UnifiedSerie(name, com_one_series.ErrorMessage, {}, tuple()))
                continue

            metadata: Dict[str, Any] = {}
            com_metadata = com_one_series.Metadata
            for names_and_description in com_metadata.ListNames():
                metadata_name = names_and_description[0]
                values = com_metadata.GetValues(metadata_name)
                if len(values) == 1:
                    metadata[metadata_name] = values[0]
                else:
                    metadata[metadata_name] = list(values)

            series.append(
                UnifiedSerie(
                    name,
                    "",
                    metadata,
                    tuple(
                        map(
                            lambda x: None if x is not None and isnan(x) else x,
                            com_one_series.Values,
                        )
                    ),
                )
            )

        ret = UnifiedSeries(series, dates)

        errors = ret.get_errors()
        raise_error = self.raise_error if raise_error is None else raise_error
        if raise_error and len(errors) != 0:
            raise GetEntitiesError(errors)

        return ret
