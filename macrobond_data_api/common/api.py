# -*- coding: utf-8 -*-

"""
The class `macrobond_data_api.common.api.Api` defines the core methods to interact with the
Macrobond database.
"""

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
    UnifiedSeriesList,
    GetAllVintageSeriesResult,
    SeriesObservationHistory,
)

from .enums import SeriesFrequency, SeriesWeekdays, CalendarMergeMode


class Api(ABC):
    # fmt: off
    """
    Common API to interact with the Macrobond database.  
    This class defines abstract methods that are implemented for both the Web API and
    Desktop COM API. You typically access them via an instance of
    `macrobond_data_api.web.web_client.WebClient` or
    `macrobond_data_api.com.com_client.ComClient`.

    Metadata methods:  
        `macrobond_data_api.common.api.Api.metadata_list_values`  
        `macrobond_data_api.common.api.Api.metadata_get_attribute_information`  
        `macrobond_data_api.common.api.Api.metadata_get_value_information`  

    Series methods:  
        `macrobond_data_api.common.api.Api.get_one_series`  
        `macrobond_data_api.common.api.Api.get_series`  
        `macrobond_data_api.common.api.Api.get_one_entity`  
        `macrobond_data_api.common.api.Api.get_entities`  
        `macrobond_data_api.common.api.Api.get_unified_series`  

    Series revision methods:  
        `macrobond_data_api.common.api.Api.get_revision_info`  
        `macrobond_data_api.common.api.Api.get_vintage_series`  
        `macrobond_data_api.common.api.Api.get_nth_release`  
        `macrobond_data_api.common.api.Api.get_all_vintage_series`  
        `macrobond_data_api.common.api.Api.get_observation_history`  

    Search methods:  
        `macrobond_data_api.common.api.Api.entity_search`  
        `macrobond_data_api.common.api.Api.entity_search_multi_filter`  


    """
    # fmt: on

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

    @abstractmethod
    def metadata_get_attribute_information(self, *names: str) -> List[MetadataAttributeInformation]:
        # pylint: disable=line-too-long
        # fmt: off
        """
        Get information about metadata attributes.

        Parameters
        ----------
        *names : str
            One or more names of metadata attributes.

        Returns
        -------
        `List[macrobond_data_api.common.types.metadata_attribute_information.MetadataAttributeInformation]`  
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
        # pylint: enable=line-too-long
        # fmt: on

    @abstractmethod
    def metadata_get_value_information(
        self, *name_val: Tuple[str, str]
    ) -> List[MetadataValueInformationItem]:
        # pylint: disable=line-too-long
        # fmt: off
        """
        Get information about metadata values.

        Parameters
        ----------
        *name_val : Tuple[str, str]
            The attribute name and a value.

        Returns
        -------
        `List[macrobond_data_api.common.types.metadata_value_information.MetadataValueInformationItem]`  
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
        # fmt: on
        # pylint: enable=line-too-long

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
            If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

        Returns
        -------
        `List[macrobond_data_api.common.types.revision_info.RevisionInfo]`
        The result is in the sane order as in the request.
        """

    @abstractmethod
    def get_vintage_series(
        self, time: datetime, *series_names: str, raise_error: bool = None
    ) -> List[VintageSeries]:
        """
        Fetch vintage series.

        Parameters
        ----------
        time : datetime
            The time of the vintage to return.
        series_name : str
            One or more names of series.
        raise_error : bool
            If True, accessing the resulting series raises a GetEntitiesError.
            If False you should inspect the is_error property of the result instead.
            If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

        Returns
        -------
        `List[macrobond_data_api.common.types.vintage_series.VintageSeries]`
        The result is in the same order as in the request.
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
            If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

        Returns
        -------
        `List[macrobond_data_api.common.types.series.Series]`
        The result is in the same order as in the request.
        """

    @abstractmethod
    def get_all_vintage_series(self, series_name: str) -> GetAllVintageSeriesResult:
        ...

    @abstractmethod
    def get_observation_history(
        self, serie_name: str, *times: datetime
    ) -> List[SeriesObservationHistory]:
        ...

    # Search

    def entity_search(
        self,
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
            no_metadata=no_metadata,
        )

    @abstractmethod
    def entity_search_multi_filter(
        self, *filters: SearchFilter, include_discontinued: bool = False, no_metadata: bool = False
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

        Returns
        -------
        `macrobond_data_api.common.types.search_result.SearchResult`
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
            If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

        Returns
        -------
        `macrobond_data_api.common.types.series.Series`
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
            If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

        Returns
        -------
        `List[macrobond_data_api.common.types.series.Series]`
        The result is in the same order as in the request.
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
            If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

        Returns
        -------
        `macrobond_data_api.common.types.entity.Entity`
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
            If None, it will use the global value `macrobond_data_api.common.api.Api.raise_error`

        Returns
        -------
        `List[macrobond_data_api.common.types.entity.Entity]`
        The result is in the same order as in the request.
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
    ) -> UnifiedSeriesList:
        # pylint: disable=line-too-long
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
        # pylint: enable=line-too-long
