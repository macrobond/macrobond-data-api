# -*- coding: utf-8 -*-

from typing import Dict, Sequence, Union
from abc import ABC, abstractmethod

from datetime import datetime

from .typs import SearchFilter, SearchResult, StartOrEndPoint, SeriesEntrie

from .enums import SeriesFrequency, SeriesWeekdays, CalendarMergeMode

from .api_return_typs import (
    GetAttributeInformationReturn,
    ListValuesReturn,
    GetRevisionInfoReturn,
    GetVintageSeriesReturn,
    #  GetObservationHistoryReturn,
    #  GetNthReleaseReturn,
    GetOneEntitieReturn,
    GetOneSeriesReturn,
    GetEntitiesReturn,
    GetSeriesReturn,
    GetUnifiedSeriesReturn,
)


class Api(ABC):
    """"""

    def __init__(self) -> None:
        self.raise_error = True

    # metadata

    # ToDo: @mb-jp Need a new name
    @abstractmethod
    def list_values(self, name: str) -> ListValuesReturn:
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
            print(api.list_values('RateType').list_of_dicts())

            # as data_frame
            print(api.list_values('RateType').data_frame())

            # as objects
            print(api.list_values('RateType').list_of_objects())
        ```
        """

    @abstractmethod
    def get_attribute_information(self, name: str) -> GetAttributeInformationReturn:
        """Get information about a type of metadata."""

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

    # not done
    # @abstractmethod
    # def get_observation_history(
    #     self, serie_name: str, time: datetime, raise_error: bool = None
    # ) -> GetObservationHistoryReturn:
    #     """"""

    # not done
    # @abstractmethod
    # def get_nth_release(
    #     self, serie_name: str, nth: int, raise_error: bool = None
    # ) -> GetNthReleaseReturn:
    #     ...  # pragma: no cover

    # Search

    def search(
        self,
        text: str = None,
        entity_types: Union[Sequence[str], str] = None,
        must_have_values: Dict[str, object] = None,
        must_not_have_values: Dict[str, object] = None,
        must_have_attributes: Union[Sequence[str], str] = None,
        must_not_have_attributes: Union[Sequence[str], str] = None,
        include_discontinued: bool = False,
    ) -> SearchResult:
        """"""
        return self.series_multi_filter(
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
    def series_multi_filter(
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
    def get_one_entitie(
        self, entity_name: str, raise_error: bool = None
    ) -> GetOneEntitieReturn:
        """Download one entity."""

    @abstractmethod
    def get_entities(
        self, *entity_names: str, raise_error: bool = None
    ) -> GetEntitiesReturn:
        """Download one or more entitys."""

    @abstractmethod
    def get_unified_series(
        self,
        *series_entries: Union[SeriesEntrie, str],
        frequency=SeriesFrequency.HIGHEST,
        weekdays=SeriesWeekdays.FULL_WEEK,
        calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ANY,
        currency="",
        start_point: StartOrEndPoint = None,
        end_point: StartOrEndPoint = None,
        raise_error: bool = None
    ) -> GetUnifiedSeriesReturn:
        """"""
