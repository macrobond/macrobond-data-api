# -*- coding: utf-8 -*-

from typing import Sequence, Union, Tuple, Dict
from abc import ABC, abstractmethod

from datetime import datetime

from .types import SearchFilter, SearchResult, StartOrEndPoint, SeriesEntry

from .enums import SeriesFrequency, SeriesWeekdays, CalendarMergeMode

from .api_return_types import (
    GetAttributeInformationReturn,
    ListValuesReturn,
    GetRevisionInfoReturn,
    GetVintageSeriesReturn,
    GetValueInformationReturn,
    GetNthReleaseReturn,
    GetOneEntityReturn,
    GetOneSeriesReturn,
    GetEntitiesReturn,
    GetSeriesReturn,
    GetUnifiedSeriesReturn,
)


class Api(ABC):
    """
    Common API to interact with the Macrobond database
    """

    def __init__(self) -> None:
        self.raise_error = True

    # metadata

    @abstractmethod
    def metadata_list_values(self, name: str) -> ListValuesReturn:
        """
        List all metadata attribute values of an attribute that uses a value list.

        Parameters
        ----------
        name : str
            The name of the metadata attribute

        Returns
        -------
        `macrobond_financial.common.api_return_types.list_values_return.ListValuesReturn`

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

    # TODO: @mb-to Wouldn't it be better if you could specify several names (such as Union[Sequence[str], str])? This is possible in the WebAPI and is more efficient.

    @abstractmethod
    def metadata_get_attribute_information(
        self, name: str
    ) -> GetAttributeInformationReturn:
        """
        Get information about a type of metadata.
        """

    @abstractmethod
    def metadata_get_value_information(
        self, *name_val: Tuple[str, str]
    ) -> GetValueInformationReturn:
        """
        Get information about metadata values.

        Parameters
        ----------
        name_val : Tuple[str, str]
            The attribute name and a value.

        Returns
        -------
        `macrobond_financial.common.api_return_types.get_value_information_return.GetValueInformationReturn`
        """

    # revision

    @abstractmethod
    def get_revision_info(
        self, *series_names: str, raise_error: bool = None
    ) -> GetRevisionInfoReturn:
        """"""

    @abstractmethod
    def get_vintage_series(
        self, serie_name: str, time: datetime, raise_error: bool = None
    ) -> GetVintageSeriesReturn:
        """"""

    @abstractmethod
    def get_nth_release(
        self, serie_name: str, nth: int, raise_error: bool = None
    ) -> GetNthReleaseReturn:
        """"""

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
        text : str
            Optional set of keywords separated by space.
        must_have_values : Dict[str, object]
            Optional dictionary of values that must be present in the entity metadata.
            The value can be a single value or an array of values. If there are several values
            for an attribute, it means that either of them must be present.
        must_not_have_values : Dict[str, object]
            Optional dictionary of values that must not be present in the entity metadata.
            The value can be a single value or an array of values.
        must_have_attributes : Union[Sequence[str], str]
            Optional set of attributes that must be present in the entity metadata.
            The value can be a single value or a sequence of values.
        must_not_have_attributes : Union[Sequence[str], str]
            Optional set of attributes that must no be present in the entity metadata.
            The value can be a single value or a sequence of values.
        include_discontinued : bool
            Set this value to True in order to include discontinued entities in the search.

        Returns
        -------
        `macrobond_financial.common.types.search_result.SearchResult`
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
        *filters : SearchFilter
            One or more search filters.
        include_discontinued : bool
            Set this value to True in order to include discontinued entities in the search.

        Returns
        -------
        `macrobond_financial.common.types.search_result.SearchResult`
        """

    # Series

    # TODO: @mb-to Why is the default value of raise_error = None instead of True or False?

    @abstractmethod
    def get_one_series(
        self, series_name: str, raise_error: bool = None
    ) -> GetOneSeriesReturn:
        """
        Download one series.

        Parameters
        ----------
        series_name : str
            The name of the series.
        raise_error : bool
            If True, accessing the resulting series raises a GetEntitiesError.
            If False you should inspect the is_error property of the result instead.

        Returns
        -------
        `macrobond_financial.common.api_return_types.get_one_series_return.GetOneSeriesReturn`
        """

    @abstractmethod
    def get_series(
        self, *series_names: str, raise_error: bool = None
    ) -> GetSeriesReturn:
        """Download one or more series."""

    @abstractmethod
    def get_one_entity(
        self, entity_name: str, raise_error: bool = None
    ) -> GetOneEntityReturn:
        """Download one entity."""

    @abstractmethod
    def get_entities(
        self, *entity_names: str, raise_error: bool = None
    ) -> GetEntitiesReturn:
        """Download one or more entitys."""

    @abstractmethod
    def get_unified_series(
        self,
        *series_entries: Union[SeriesEntry, str],
        frequency=SeriesFrequency.HIGHEST,
        weekdays=SeriesWeekdays.FULL_WEEK,
        calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ANY,
        currency="",
        start_point: StartOrEndPoint = None,
        end_point: StartOrEndPoint = None,
        raise_error: bool = None
    ) -> GetUnifiedSeriesReturn:
        """Get one or more series and convert them to a common frequency and calendar"""
