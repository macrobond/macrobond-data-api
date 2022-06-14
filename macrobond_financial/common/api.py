# -*- coding: utf-8 -*-

from typing import List, Sequence, Union, Tuple, Dict
from abc import ABC, abstractmethod

from datetime import datetime

from .types import (
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
    UnifiedSeries,
)

from .enums import SeriesFrequency, SeriesWeekdays, CalendarMergeMode


class Api(ABC):
    """
    Common API to interact with the Macrobond database.
    """

    def __init__(self) -> None:
        self.raise_error = True
        """
        Controls the default value of the parameter called raise_error, which is used in many
        API calls. The default value is "True".
        """

    # metadata

    @abstractmethod
    def metadata_list_values(self, name: str) -> MetadataValueInformation:
        """
        List all metadata attribute values of an attribute that uses a value list.

        Parameters
        ----------
        name : str
            The name of the metadata attribute

        Returns
        -------
        `MetadataValueInformation`

        Examples
        -------
        ```python
        with ComClient() as api: # or WebClient

            # as dict
            print(api.metadata_list_values('RateType').list_of_dicts())

            # as data_frame
            print(api.metadata_list_values('RateType').data_frame())

            # as objects
            print(api.metadata_list_values('RateType').list_of_objects())
        ```
        """

    @abstractmethod
    def metadata_get_attribute_information(
        self, *names: str
    ) -> Sequence[MetadataAttributeInformation]:
        """
        Get information about metadata attributes.
        """

    @abstractmethod
    def metadata_get_value_information(
        self, *name_val: Tuple[str, str]
    ) -> List[MetadataValueInformationItem]:
        """
        Get information about metadata values.

        Parameters
        ----------
        *name_val : Tuple[str, str]
            The attribute name and a value.

        Returns
        -------
        `List[MetadataValueInformationItem]`
        """

    # revision

    @abstractmethod
    def get_revision_info(self, *series_names: str, raise_error: bool = None) -> List[RevisionInfo]:
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
            If None, it will use the global value `macrobond_financial.common.api.Api.raise_error`

        Returns
        -------
        `List[RevisionInfo]`
        """

    @abstractmethod
    def get_vintage_series(
        self, time: datetime, *series_names: str, raise_error: bool = None
    ) -> List[VintageSeries]:
        """
        Fetch a vintage series.

        Parameters
        ----------
        time : datetime
            The time of the vintage to return.
        series_name : str
            One or more names of series.
        raise_error : bool
            If True, accessing the resulting series raises a GetEntitiesError.
            If False you should inspect the is_error property of the result instead.
            If None, it will use the global value `macrobond_financial.common.api.Api.raise_error`

        Returns
        -------
        `List[VintageSeries]`
        """

    @abstractmethod
    def get_nth_release(
        self, nth: int, *series_names: str, raise_error: bool = None
    ) -> List[Series]:
        """
        Fetcha series where each value is the nth change of the value.

        Parameters
        ----------
        time : nth
            The nth change of each value.
        series_names : str
            One or more names of series.
        raise_error : bool
            If True, accessing the resulting series raises a GetEntitiesError.
            If False you should inspect the is_error property of the result instead.
            If None, it will use the global value `macrobond_financial.common.api.Api.raise_error`

        Returns
        -------
        `List[Series]`
        """

    # TODO: @mb-to We should add a method get_all_vintage_series that takes _one_ series name.

    # Search

    # TODO: @mb-to We should consider to add noMetaData as a parameter, even if is used only in Web

    def entity_search(
        self,
        text: str = None,
        entity_types: Union[Sequence[str], str] = None,
        must_have_values: Dict[str, object] = None,
        must_not_have_values: Dict[str, object] = None,
        must_have_attributes: Union[Sequence[str], str] = None,
        must_not_have_attributes: Union[Sequence[str], str] = None,
        include_discontinued: bool = False,
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
        `SearchResult`
        """
        return self.entity_search_multi_filter(
            SearchFilter(
                text=text,
                entity_types=entity_types,
                must_have_values=must_have_values,
                must_not_have_values=must_not_have_values,
                must_have_attributes=must_have_attributes,
                must_not_have_attributes=must_not_have_attributes,
            ),
            include_discontinued=include_discontinued,
        )

    @abstractmethod
    def entity_search_multi_filter(
        self, *filters: SearchFilter, include_discontinued: bool = False
    ) -> SearchResult:
        """
        Search for time series and other entitites.
        You can pass more than one search filter. In this case the filters have to use different
        entity types and searches will be nested so that the result of the previous filter will be
        used as a condition in the subsequent filter linked by the entity type.

        Parameters
        ----------
        *filters : `macrobond_financial.common.types.search_filter.SearchFilter`
            One or more search filters.
        include_discontinued : bool
            Set this value to True in order to include discontinued entities in the search.

        Returns
        -------
        `macrobond_financial.common.types.search_result.SearchResult`
        """

    # Series

    @abstractmethod
    def get_one_series(self, series_name: str, raise_error: bool = None) -> Series:
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
            If None, it will use the global value `macrobond_financial.common.api.Api.raise_error`

        Returns
        -------
        `Series`
        """

    @abstractmethod
    def get_series(self, *series_names: str, raise_error: bool = None) -> List[Series]:
        """
        Download one or more series.

        .. Important:: It is much more efficient to download more than one series at a time.
           However, downloading too many at a time is less efficient and can exhaust memory.
           A good habit is to download series in batches of around 200.

        Parameters
        ----------
        *series_names : str
            One or more names of series.
        raise_error : bool
            If True, accessing the resulting series raises a GetEntitiesError.
            If False you should inspect the is_error property of the result instead.
            If None, it will use the global value `macrobond_financial.common.api.Api.raise_error`

        Returns
        -------
        `List[Series]`
        """

    @abstractmethod
    def get_one_entity(self, entity_name: str, raise_error: bool = None) -> Entity:
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
            If None, it will use the global value `macrobond_financial.common.api.Api.raise_error`

        Returns
        -------
        `Entity`
        """

    @abstractmethod
    def get_entities(self, *entity_names: str, raise_error: bool = None) -> List[Entity]:
        """
        Download one or more entities.

        .. Important:: It is much more efficient to download more than one entity at a time.
           However, downloading too many at a time is less efficient and can exhaust memory.
           A good habit is to download entities in batches of around 200.

        Parameters
        ----------
        *entity_names : str
            One or more names of entities.
        raise_error : bool
            If True, accessing the resulting entities raises a GetEntitiesError.
            If False you should inspect the is_error property of the result instead.
            If None, it will use the global value `macrobond_financial.common.api.Api.raise_error`

        Returns
        -------
        `List[Entity]`
        """

    @abstractmethod
    def get_unified_series(
        self,
        *series_entries: Union[SeriesEntry, str],
        frequency=SeriesFrequency.HIGHEST,
        weekdays=SeriesWeekdays.MONDAY_TO_FRIDAY,
        calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ANY,
        currency="",
        start_point: StartOrEndPoint = None,
        end_point: StartOrEndPoint = None,
        raise_error: bool = None
    ) -> UnifiedSeries:
        """
        Get one or more series and convert them to a common frequency and calendar.

        Parameters
        ----------
        *series_entries : Union[SeriesEntry, str]
            One or more names of series or
            `macrobond_financial.common.types.series_entry.SeriesEntry` objects.
        frequency : `macrobond_financial.common.enums.series_frequency.SeriesFrequency`
            Specifies what frequency the series should be converted to.
            By default, it will be converted to the highest frequency of any series.
        weekdays : `macrobond_financial.common.enums.series_weekdays.SeriesWeekdays`
            The days of the week used for daily series. The default is Monday to Friday.
        calendar_merge_mode : `macrobond_financial.common.enums.calendar_merge_mode.CalendarMergeMode`
            The start date mode determines how the start date is calculated.
            By default the mode is to start when there is data in any series.
        currency : str
            The currency to use for currency conversion or omitted for no conversion.
        start_point : `macrobond_financial.common.types.start_or_end_point.StartOrEndPoint`
            The start point. By default, this is determined by the startDateMode.
        end_point : `macrobond_financial.common.types.start_or_end_point.StartOrEndPoint`
            The end point. By default, this is determined by the endDateMode.
        raise_error : bool
            If True, accessing the resulting entities raises a GetEntitiesError.
            If False you should inspect the is_error property of the result instead.
            If None, it will use the global value `macrobond_financial.common.api.Api.raise_error`

        Returns
        -------
        `UnifiedSeries`
        """
