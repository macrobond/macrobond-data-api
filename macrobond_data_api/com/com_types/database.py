# pylint: disable = invalid-name , missing-module-docstring , too-many-arguments
# mypy: disable_error_code = empty-body

from typing import List, Union, Tuple, Sequence

from .series import Series
from .entity import Entity
from .series_request import SeriesRequest
from .metadata import Metadata
from .metadata_information import MetadataInformation
from .search_query import SearchQuery
from .search_result import SearchResult
from .series_with_revisions import SeriesWithRevisions


class Database:
    """This interface allows you to interact with the Macrobond database."""

    def FetchOneSeries(self, series_name: str) -> Series:
        """Download one series from the database."""

    def FetchSeries(self, series_names: Union[str, Tuple[str, ...], SeriesRequest]) -> Tuple[Series, ...]:
        """
        Download one or more series from the database.
        The parameter can be a string, a vector of series names or an
        object created by 'CreateUnifiedSeriesRequest()'.
        The result is a vector of series in the same order as requested.
        """

    def FetchOneEntity(self, entity_name: str) -> Entity:
        """Download an entity, such as a Release."""

    def FetchEntities(self, entity_names: Union[str, Tuple[str, ...]]) -> Tuple[Entity, ...]:
        """
        Download one or more entities from the database.
        The parameter can be a string or a list of entity names. The result is a vector
        of entities in the same order as requested.
        """

    def CreateUnifiedSeriesRequest(self) -> SeriesRequest:
        """
        Create a request of one or more series where the resulting time series will be
        converted to a common length and calendar.
        You can specify frequency, currency, date range, missing value and
        frequency conversion methods
        """

    def CreateSeriesObject(
        self,
        name: str,
        description: str,
        region: str,
        category: str,
        frequency: int,
        dayMask: int,
        startDateOrDates: object,
        values: object,
        metadata: Metadata,
    ) -> Series:
        """
        Create a series object that can be uploaded to the server using
        the 'UploadOneOrMoreSeries()' method.
        The startDateOrDates can either be just one start date or one date for each value.
        It is recommended to use timezone UTC for these dates.
        The values should be an array of numbers.
        The region is a value of the Region metadata which is based on the 2 letter ISO for
        countries. See list here.
        The metadata parameter is optional.
        The name should be of the form "ih:storage:id", where storage
        is "priv", "dept" or "com" coresponding to the private, department and company storages.
        Id should must be a unique identifier per storage.
        """

    def CreateSeriesObjectWithForecastFlags(
        self,
        name: str,
        description: str,
        region: str,
        category: str,
        frequency: int,
        dayMask: int,
        startDateOrDates: object,
        values: object,
        forecastFlags: object,
        metadata: Metadata,
    ) -> Series:
        """
        Create a series object that can be uploaded to the server using the
        UploadOneOrMoreSeries method.
        The startDateOrDates can either be just one start date or one date for each value.
        It is recommended to use timezone UTC for these dates.
        The values should be an array of numbers.
        The forecastFlags should be an array of boolean values where true means that the
        corresponding value is a forecast.
        The region is a value of the Region metadata which is based on the 2 letter ISO
        for countries. See list here.
        The metadata parameter is optional.
        The name should be of the form "ih:storage:id",
        where storage is "priv", "dept" or "com" coresponding to the private,
        department and company storages.
        Id should must be a unique identifier per storage.
        """

    def UploadOneOrMoreSeries(self, series: Union[Series, List[Series]]) -> None:
        """
        Upload one or more series created by the CreateSeriesObject method.
        The parameter can be a single series or a list of series.
        It is more efficient to upload more series at once than one by one.
        """

    def DeleteOneOrMoreSeries(self, name_or_names: Union[str, List[str]]) -> None:
        """
        Delete one or more series.
        The parameter can be a single series name or a list of names.
        It is more efficient to delete more than one series at once than one by one.
        """

    def CreateEmptyMetadata(self) -> Metadata:
        """
        Create an empty set of metadata. The content can be changed until it is used in a series.
        """

    def CreateDerivedMetadata(self, metadata: Metadata) -> Metadata:
        """
        Create a set of metadata derived from another set. The content can be changed until it
        is used in a series.
        """

    def GetMetadataInformation(self, name: str) -> MetadataInformation:
        """Get information about a type of metadata."""

    def CreateSearchQuery(self) -> SearchQuery:
        """
        Create a search query object.
        Set properties on this object and pass it to the Search function in order to
        search for series and other entities.
        (MB 1.23 or later. Requires Data+ license.)
        """

    def Search(self, queries: List[SearchQuery]) -> SearchResult:
        """
        Execute a search for series and other entities. See specification
        of ISearchQuery for details.
        (MB 1.23 or later. Requires Data+ license.)
        """

    def FetchOneSeriesWithRevisions(self, name: str) -> SeriesWithRevisions:
        """
        Download one revision history for one series.
        (MB 1.23 or later. Requires Data+ license.)
        """

    def FetchSeriesWithRevisions(self, seriesNames: Union[str, Sequence[str]]) -> Tuple[SeriesWithRevisions, ...]:
        """
        Download one or more series from the database.
        The parameter can be a string or a vector of series names.
        The result is a vector of revision history objects in the same order as requested.
        (MB 1.23 or later. Requires Data+ license.)
        """
