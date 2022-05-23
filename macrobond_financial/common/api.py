# -*- coding: utf-8 -*-

from typing import Sequence, Union, Tuple, Dict
from abc import ABC, abstractmethod

from datetime import datetime

from .typs import SearchFilter, SearchResult, StartOrEndPoint, SeriesEntry

from .enums import SeriesFrequency, SeriesWeekdays, CalendarMergeMode

from .api_return_typs import (
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
        List all metadata attribute values.

        Parameters
        ----------
        name : str
            record that failed processing

        Returns
        -------
        `macrobond_financial.common.api_return_typs.list_values_return.ListValuesReturn`

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
        self, name: str
    ) -> GetAttributeInformationReturn:
        """Get information about a type of metadata."""

    @abstractmethod
    def metadata_get_value_information(
        self, *name_val: Tuple[str, str]
    ) -> GetValueInformationReturn:
        """"""

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
        """Search for time series and other entitites."""
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
        """"""

    # Series

    @abstractmethod
    def get_one_series(
        self, series_name: str, raise_error: bool = None
    ) -> GetOneSeriesReturn:
        """Download one series."""

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
