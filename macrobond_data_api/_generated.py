#
# This is generated code, do not edit
#

from typing import Generator, Sequence, Union, Tuple, Dict, Optional
from datetime import datetime
from macrobond_data_api.common.types import (
    SearchFilter,
    SearchResult,
    StartOrEndPoint,
    SeriesEntry,
    MetadataValueInformation,
    MetadataAttributeInformation,
    MetadataValueInformationItem,
    RevisionInfo,
    VintageSeries,
    Series,
    Entity,
    UnifiedSeriesList,
    GetAllVintageSeriesResult,
    SeriesObservationHistory,
    SeriesWithVintages,
    RevisionHistoryRequest,
)
from macrobond_data_api.common.enums import SeriesFrequency, SeriesWeekdays, CalendarMergeMode
from ._get_api import _get_api


def delete_serie(series_name: str) -> None:
    """
    Delete one series.

    Parameters
    ----------
    series_name : str
        The name of the series.

    Returns
    -------
    `None`
    """
    return _get_api().delete_serie(series_name)


def entity_search(
    text: str = None,
    entity_types: Union[Sequence[str], str] = None,
    must_have_values: Dict[str, object] = None,
    must_not_have_values: Dict[str, object] = None,
    must_have_attributes: Union[Sequence[str], str] = None,
    must_not_have_attributes: Union[Sequence[str], str] = None,
    include_discontinued: bool = False,
    no_metadata: bool = False,
) -> SearchResult:
    """
    Search for time series and other entitites.

    Parameters
    ----------
    text: str
        Optional set of keywords separated by space.
    must_have_values: Dict[str, object]
        Optional dictionary of values that must be present in the entity metadata.
        The value can be a single value or an array of values. If there are several values
        for an attribute, it means that either of them must be present.
    must_not_have_values: Dict[str, object]
        Optional dictionary of values that must not be present in the entity metadata.
        The value can be a single value or an array of values.
    must_have_attributes: Union[Sequence[str], str]
        Optional set of attributes that must be present in the entity metadata.
        The value can be a single value or a sequence of values.
    must_not_have_attributes: Union[Sequence[str], str]
        Optional set of attributes that must no be present in the entity metadata.
        The value can be a single value or a sequence of values.
    include_discontinued: bool
        Set this value to True in order to include discontinued entities in the search.

    Returns
    -------
    `macrobond_data_api.common.types.search_result.SearchResult`
    """
    return _get_api().entity_search(
        text,
        entity_types,
        must_have_values,
        must_not_have_values,
        must_have_attributes,
        must_not_have_attributes,
        include_discontinued,
        no_metadata,
    )


def entity_search_multi_filter(
    *filters: SearchFilter, include_discontinued: bool = False, no_metadata: bool = False
) -> SearchResult:
    """
    Search for time series and other entitites.
    You can pass more than one search filter. In this case the filters have to use different
    entity types and searches will be nested so that the result of the previous filter will be
    used as a condition in the subsequent filter linked by the entity type.

    Parameters
    ----------
    *filters : `macrobond_data_api.common.types.search_filter.SearchFilter`
        One or more search filters.
    include_discontinued : bool
        Set this value to True in order to include discontinued entities in the search.
    no_metadata : bool
        Set this value to True in order only return the entity names and no metadata, which is faster.

    Returns
    -------
    `macrobond_data_api.common.types.search_result.SearchResult`
    """
    return _get_api().entity_search_multi_filter(
        *filters, include_discontinued=include_discontinued, no_metadata=no_metadata
    )


def get_all_vintage_series(series_name: str) -> GetAllVintageSeriesResult:
    """
    Get all vintages of a series.

    Parameters
    ----------
    series_name : str
        The name of the series.

    Returns
    -------
    `macrobond_data_api.common.types.get_all_vintage_series_result.GetAllVintageSeriesResult`
    """
    return _get_api().get_all_vintage_series(series_name)


def get_entities(entity_names: Sequence[str], raise_error: bool = None) -> Sequence[Entity]:
    """
    Download one or more entities.

    .. Important:: It is much more efficient to download more than one entity at a time.
       However, downloading too many at a time is less efficient and can exhaust memory.
       A good habit is to download entities in batches of around 200.

    Parameters
    ----------
    entity_names : Sequence[str]
        The names of the entities.
    raise_error : bool
        If True, accessing the resulting entities raises a GetEntitiesError.
        If False you should inspect the is_error property of the result instead.
        If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

    Returns
    -------
    `Sequence[macrobond_data_api.common.types.entity.Entity]`
    The result is in the same order as in the request.
    """
    return _get_api().get_entities(entity_names, raise_error)


def get_many_series(
    series: Sequence[Union[str, Tuple[str, Optional[datetime]]]], include_not_modified: bool = False
) -> Generator[Series, None, None]:
    """
    Parameters
    ----------
    series: `Sequence[Union[str, Tuple[str, Optional[datetime]]]]`
        A sequence of series names or a sequence of name plus a timestamp for the last modification.
    include_not_modified: `bool`
        Set this value to True in order to include NotNodified series.

    Returns
    -------
    `Generator[Optional[macrobond_data_api.common.types.series.Series]]`
    """
    return _get_api().get_many_series(series, include_not_modified)


def get_many_series_with_revisions(
    requests: Sequence[RevisionHistoryRequest], include_not_modified: bool = False
) -> Generator[SeriesWithVintages, None, None]:
    """
    Download all revisions for one or more series.
    Specify a callback to receive the response series by series.
    This method is primarily intended for syncronizing a local database with updates.

    You are expected to retain the LastModifiedTimeStamp, LastRevisionTimeStamp and LastRevisionAdjustmentTimeStamp
    for each series and use them in the next request. The attributes LastRevisionTimeStamp and
    LastRevisionAdjustmentTimeStamp might not be present in all responses.

    This function returns a generator that will return the result in a streaming fashion to conserve memory since
    the result can be very large.

    Parameters
    ----------
    requests: `Sequence[macrobond_data_api.common.types.revision_history_request.RevisionHistoryRequest]`
        A sequence of series requests.
    include_not_modified: `bool`
        Set this value to True in order to include NotNodified series.

    Returns
    -------
    `Generator[macrobond_data_api.common.types.series_with_vintages.SeriesWithVintages]`
    """
    return _get_api().get_many_series_with_revisions(requests, include_not_modified)


def get_nth_release(
    nth: int, series_names: Sequence[str], include_times_of_change: bool = False, raise_error: bool = None
) -> Sequence[Series]:
    """
    Get one or more series where each value is the nth change of the value.

    Parameters
    ----------
    time : nth
        The nth change of each value.
    series_names : str
        The names of the series.
    include_times_of_change : bool
        Include information of the time each values was last changed.
    raise_error : bool
        If True, accessing the resulting series raises a GetEntitiesError.
        If False you should inspect the is_error property of the result instead.
        If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

    Returns
    -------
    `Sequence[macrobond_data_api.common.types.series.Series]`
    The result is in the same order as in the request.
    """
    return _get_api().get_nth_release(nth, series_names, include_times_of_change, raise_error)


def get_observation_history(series_name: str, *times: datetime) -> Sequence[SeriesObservationHistory]:
    """
    Get the revision of an observation.

    Parameters
    ----------
    series_name : str
        The name of the series.
    times : datetime
        One or more timestamps.

    Returns
    -------
    `Sequence[macrobond_data_api.common.types.series_observation_history.SeriesObservationHistory]`
    """
    return _get_api().get_observation_history(series_name, *times)


def get_one_entity(entity_name: str, raise_error: bool = None) -> Entity:
    """
    Download one entity.

    .. important:: It is much more efficient to download more than one entity at a time.
       See `Api.get_entities`.

    Parameters
    ----------
    entity_name : str
        The name the entity.
    raise_error : bool
        If True, accessing the resulting entity raises a GetEntitiesError.
        If False you should inspect the is_error property of the result instead.
        If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

    Returns
    -------
    `macrobond_data_api.common.types.entity.Entity`
    """
    return _get_api().get_one_entity(entity_name, raise_error)


def get_one_nth_release(
    nth: int, series_name: str, include_times_of_change: bool = False, raise_error: bool = None
) -> Series:
    """
    Get a series where each value is the nth change of the value.

    Parameters
    ----------
    time : nth
        The nth change of each value.
    series_name : str
        The name of the series.
    include_times_of_change : bool
        Include information of the time each values was last changed.
    raise_error : bool
        If True, accessing the resulting series raises a GetEntitiesError.
        If False you should inspect the is_error property of the result instead.
        If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

    Returns
    -------
    `macrobond_data_api.common.types.series.Series`
    """
    return _get_api().get_one_nth_release(nth, series_name, include_times_of_change, raise_error)


def get_one_series(series_name: str, raise_error: bool = None) -> Series:
    """
    Download one series.

    .. important:: It is much more efficient to download more than one series at a time.
       See `Api.get_series`.

    Parameters
    ----------
    series_name : str
        The name of the series.
    raise_error : bool
        If True, accessing the resulting series raises a GetEntitiesError.
        If False you should inspect the is_error property of the result instead.
        If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

    Returns
    -------
    `macrobond_data_api.common.types.series.Series`
    """
    return _get_api().get_one_series(series_name, raise_error)


def get_one_vintage_series(
    time: datetime, series_name: str, include_times_of_change: bool = False, raise_error: bool = None
) -> VintageSeries:
    """
    Get one vintage series.

    Parameters
    ----------
    time : datetime
        The time of the vintage to return.
    series_name : str
        The name of the series.
    include_times_of_change : bool
        Include information of the time each values was last changed.
    raise_error : bool
        If True, accessing the resulting series raises a GetEntitiesError.
        If False you should inspect the is_error property of the result instead.
        If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

    Returns
    -------
    `macrobond_data_api.common.types.vintage_series.VintageSeries`
    """
    return _get_api().get_one_vintage_series(time, series_name, include_times_of_change, raise_error)


def get_revision_info(*series_names: str, raise_error: bool = None) -> Sequence[RevisionInfo]:
    """
    Get information about if revision history is available for a series
    and a list of revision timestamps.

    Parameters
    ----------
    *series_names : str
        One or more series names.
    raise_error : bool
        If True, accessing the resulting series raises a GetEntitiesError.
        If False you should inspect the is_error property of the result instead.
        If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

    Returns
    -------
    `Sequence[macrobond_data_api.common.types.revision_info.RevisionInfo]`
    The result is in the sane order as in the request.
    """
    return _get_api().get_revision_info(*series_names, raise_error=raise_error)


def get_series(series_names: Sequence[str], raise_error: bool = None) -> Sequence[Series]:
    """
    Download one or more series.

    .. Important:: It is much more efficient to download more than one series at a time.
       However, downloading too many at a time is less efficient and can exhaust memory.
       A good habit is to download series in batches of around 200.

    Parameters
    ----------
    series_names : Sequence[str]
        The names of the series.
    raise_error : bool
        If True, accessing the resulting series raises a GetEntitiesError.
        If False you should inspect the is_error property of the result instead.
        If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

    Returns
    -------
    `Sequence[macrobond_data_api.common.types.series.Series]`
    The result is in the same order as in the request.
    """
    return _get_api().get_series(series_names, raise_error)


def get_unified_series(
    *series_entries: Union[SeriesEntry, str],
    frequency: SeriesFrequency = SeriesFrequency.HIGHEST,
    weekdays: SeriesWeekdays = SeriesWeekdays.MONDAY_TO_FRIDAY,
    calendar_merge_mode: CalendarMergeMode = CalendarMergeMode.AVAILABLE_IN_ANY,
    currency: str = "",
    start_point: StartOrEndPoint = None,
    end_point: StartOrEndPoint = None,
    raise_error: bool = None
) -> UnifiedSeriesList:
    """
    Get one or more series and convert them to a common frequency and calendar.

    Parameters
    ----------
    *series_entries : Union[macrobond_data_api.common.types.series_entry.SeriesEntry, str]
        One or more names of series or
        `macrobond_data_api.common.types.series_entry.SeriesEntry` objects.
    frequency : `macrobond_data_api.common.enums.series_frequency.SeriesFrequency`
        Specifies what frequency the series should be converted to.
        By default, it will be converted to the highest frequency of any series.
    weekdays : `macrobond_data_api.common.enums.series_weekdays.SeriesWeekdays`
        The days of the week used for daily series. The default is Monday to Friday.
    calendar_merge_mode : `macrobond_data_api.common.enums.calendar_merge_mode.CalendarMergeMode`
        The start date mode determines how the start date is calculated.
        By default the mode is to start when there is data in any series.
    currency : str
        The currency to use for currency conversion or omitted for no conversion.
    start_point : `macrobond_data_api.common.types.start_or_end_point.StartOrEndPoint`
        The start point. By default, this is determined by the startDateMode.
    end_point : `macrobond_data_api.common.types.start_or_end_point.StartOrEndPoint`
        The end point. By default, this is determined by the endDateMode.
    raise_error : bool
        If True, accessing the resulting entities raises a GetEntitiesError.
        If False you should inspect the is_error property of the result instead.
        If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

    Returns
    -------
    `macrobond_data_api.common.types.unified_series.UnifiedSeries`
    The result is in the same order as in the request.
    """
    return _get_api().get_unified_series(
        *series_entries,
        frequency=frequency,
        weekdays=weekdays,
        calendar_merge_mode=calendar_merge_mode,
        currency=currency,
        start_point=start_point,
        end_point=end_point,
        raise_error=raise_error
    )


def get_vintage_series(
    time: datetime,
    series_names: Sequence[str],
    include_times_of_change: bool = False,
    raise_error: bool = None,
) -> Sequence[VintageSeries]:
    """
    Get one or more vintage series.

    Parameters
    ----------
    time : datetime
        The time of the vintage to return.
    series_names : str
        The names of the series.
    include_times_of_change : bool
        Include information of the time each values was last changed.
    raise_error : bool
        If True, accessing the resulting series raises a GetEntitiesError.
        If False you should inspect the is_error property of the result instead.
        If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

    Returns
    -------
    `Sequence[macrobond_data_api.common.types.vintage_series.VintageSeries]`
    The result is in the same order as in the request.
    """
    return _get_api().get_vintage_series(time, series_names, include_times_of_change, raise_error)


def metadata_get_attribute_information(*names: str) -> Sequence[MetadataAttributeInformation]:
    """
    Get information about metadata attributes.

    Parameters
    ----------
    *names : str
        One or more names of metadata attributes.

    Returns
    -------
    `Sequence[macrobond_data_api.common.types.metadata_attribute_information.MetadataAttributeInformation]`
    The result is in the same order as the attribute names in the request.

    Examples
    -------
    ```python
    with ComClient() as api: # or WebClient

        # as objects
        print(api.metadata_get_attribute_information("Region", "Unit"))

        # as dict
        print(api.metadata_get_attribute_information("Region")[0].to_dict())

        # as data_frame
        print(api.metadata_get_attribute_information("Region")[0].to_pd_data_frame())
    ```
    """
    return _get_api().metadata_get_attribute_information(*names)


def metadata_get_value_information(*name_val: Tuple[str, str]) -> Sequence[MetadataValueInformationItem]:
    """
    Get information about metadata values.

    Parameters
    ----------
    *name_val : Tuple[str, str]
        The attribute name and a value.

    Returns
    -------
    `Sequence[macrobond_data_api.common.types.metadata_value_information.MetadataValueInformationItem]`
    The result is in the same order as the attribute names in the request.

    Examples
    -------
    ```python
    with ComClient() as api: # or WebClient

        # as objects
        print(api.metadata_get_value_information(("RateType", "mole"), ("RateType","cobe")))

        # as dict
        print(api.metadata_get_value_information(("RateType", "mole"))[0].to_dict())

        # as data_frame
        print(api.metadata_get_value_information(("RateType", "mole"))[0].to_pd_data_frame())
    ```
    """
    return _get_api().metadata_get_value_information(*name_val)


def metadata_list_values(name: str) -> MetadataValueInformation:
    """
    List all metadata attribute values of an attribute that uses a value list.

    Parameters
    ----------
    name : str
        The name of the metadata attribute

    Returns
    -------
    `macrobond_data_api.common.types.metadata_value_information.MetadataValueInformation`

    Examples
    -------
    ```python
    with ComClient() as api: # or WebClient

        # as objects
        print(api.metadata_list_values("RateType"))

        # as dict
        print(api.metadata_list_values('RateType').to_dict())

        # as data_frame
        print(metadata_list_values("RateType").to_pd_data_frame())
    ```
    """
    return _get_api().metadata_list_values(name)


def upload_series(
    name: str,
    description: str,
    region: str,
    category: str,
    frequency: SeriesFrequency,
    values: Sequence[Optional[float]],
    start_date_or_dates: Union[datetime, Sequence[datetime]],
    dayMask: SeriesWeekdays = SeriesWeekdays.MONDAY_TO_FRIDAY,
    metadata: Optional[dict] = None,
    forecast_flags: Optional[Sequence[bool]] = None,
) -> None:
    """
    Upload an in-house time series.

    Parameters
    ----------
    name : str
        The name of the series.
    description : str
        The description of the series.
    region : str
        The region of the series.
    category : str
        The category of the series.
    frequency : `macrobond_data_api.common.enums.series_frequency.SeriesFrequency`
        The frequency of the series.
    values : `Sequence[Optional[float]]`
        The values of the series.
    start_date_or_dates : `Union[datetime, Sequence[datetime]]`
        The start date of the series or dates of the series.
    dayMask : `macrobond_data_api.common.enums.series_weekdays.SeriesWeekdays`
        The days of the week used for daily series. The default is Monday to Friday.
    metadata : `Optional[dict]`
        The metadata of the series.
    forecast_flags : `Optional[Sequence[bool]]`
        The forecast flags of the series.

    Returns
    -------
    `None`
    """
    return _get_api().upload_series(
        name, description, region, category, frequency, values, start_date_or_dates, dayMask, metadata, forecast_flags
    )
