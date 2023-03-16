from typing import Generator, Sequence, Union, Tuple, Dict, Optional
from datetime import datetime

from macrobond_data_api.common import Api

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


class FakeApi(Api):
    # metadata

    def metadata_list_values(self, name: str) -> MetadataValueInformation:
        raise NotImplementedError()

    def metadata_get_attribute_information(self, *names: str) -> Sequence[MetadataAttributeInformation]:
        raise NotImplementedError()

    def metadata_get_value_information(self, *name_val: Tuple[str, str]) -> Sequence[MetadataValueInformationItem]:
        raise NotImplementedError()

    # revision

    def get_revision_info(self, *series_names: str, raise_error: bool = None) -> Sequence[RevisionInfo]:
        raise NotImplementedError()

    def get_vintage_series(
        self, time: datetime, *series_names: str, include_times_of_change: bool = False, raise_error: bool = None
    ) -> Sequence[VintageSeries]:
        raise NotImplementedError()

    def get_nth_release(
        self, nth: int, *series_names: str, include_times_of_change: bool = False, raise_error: bool = None
    ) -> Sequence[Series]:
        raise NotImplementedError()

    def get_all_vintage_series(self, series_name: str) -> GetAllVintageSeriesResult:
        raise NotImplementedError()

    def get_observation_history(self, series_name: str, *times: datetime) -> Sequence[SeriesObservationHistory]:
        raise NotImplementedError()

    def get_many_series_with_revisions(
        self, requests: Sequence[RevisionHistoryRequest], include_not_modified: bool = False
    ) -> Generator[SeriesWithVintages, None, None]:
        raise NotImplementedError()

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
        return super().entity_search(
            text=text,
            entity_types=entity_types,
            must_have_values=must_have_values,
            must_not_have_values=must_not_have_values,
            must_have_attributes=must_have_attributes,
            must_not_have_attributes=must_not_have_attributes,
            include_discontinued=include_discontinued,
            no_metadata=no_metadata,
        )

    def entity_search_multi_filter(
        self, *filters: SearchFilter, include_discontinued: bool = False, no_metadata: bool = False
    ) -> SearchResult:
        raise NotImplementedError()

    # Series

    def get_one_series(self, series_name: str, raise_error: bool = None) -> Series:
        raise NotImplementedError()

    def get_series(self, *series_names: str, raise_error: bool = None) -> Sequence[Series]:
        raise NotImplementedError()

    def get_one_entity(self, entity_name: str, raise_error: bool = None) -> Entity:
        raise NotImplementedError()

    def get_entities(self, *entity_names: str, raise_error: bool = None) -> Sequence[Entity]:
        raise NotImplementedError()

    def get_many_series(self, *series: Tuple[str, Optional[datetime]]) -> Generator[Optional[Series], None, None]:
        raise NotImplementedError()

    def get_unified_series(
        self,
        *series_entries: Union[SeriesEntry, str],
        frequency: SeriesFrequency = SeriesFrequency.HIGHEST,
        weekdays: SeriesWeekdays = SeriesWeekdays.MONDAY_TO_FRIDAY,
        calendar_merge_mode: CalendarMergeMode = CalendarMergeMode.AVAILABLE_IN_ANY,
        currency: str = "",
        start_point: StartOrEndPoint = None,
        end_point: StartOrEndPoint = None,
        raise_error: bool = None
    ) -> UnifiedSeriesList:
        raise NotImplementedError()
