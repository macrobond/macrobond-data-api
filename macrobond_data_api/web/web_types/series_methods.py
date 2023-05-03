from typing import List, Sequence, cast, TYPE_CHECKING

from datetime import datetime

if TYPE_CHECKING:  # pragma: no cover
    from requests import Response
    from ..session import Session
    from .series_response import SeriesResponse
    from .entity_response import EntityResponse
    from .entity_request import EntityRequest
    from .series_with_revisions_info_response import SeriesWithRevisionsInfoResponse
    from .vintage_series_response import VintageSeriesResponse
    from .series_with_times_of_change_response import SeriesWithTimesOfChangeResponse
    from .series_observation_history_response import SeriesObservationHistoryResponse
    from .feed_entities_response import FeedEntitiesResponse
    from .entity_info_for_display_response import EntityInfoForDisplayResponse
    from .unified_series_response import UnifiedSeriesResponse
    from .unified_series_request import UnifiedSeriesRequest
    from .revision_history_request import RevisionHistoryRequest


class SeriesMethods:
    """Time series and entity operations"""

    def __init__(self, session: "Session") -> None:
        self.__session = session

    # Get /fetchentities
    def fetch_entities(self, *entitie_names: str) -> List["EntityResponse"]:
        """
        Fetch one or more entities.
        The result will be in the same order as the request.

        OAuth scope: 'macrobond_web_api.read_mb'

        Codes:
        200 The operation was successful.
        400 The operation failed.
        401 Unauthorized. Missing, invalid or expired access token.
        403 Forbidden. Not authorized.
        """
        response = self.__session.get_or_raise("v1/series/fetchentities", params={"n": entitie_names})
        return cast(List["EntityResponse"], response.json())

    # Get /v1/series/fetchseries
    def get_fetch_series(self, *series_names: str) -> List["SeriesResponse"]:
        """
        Fetch one or more entities.
        The result will be in the same order as the request.

        OAuth scope: macrobond_web_api.read_mb

        Codes:
            200 The operation was successful.

            400 The operation failed.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.
        """
        response = self.__session.get_or_raise("v1/series/fetchseries", params={"n": series_names})
        return cast(List["SeriesResponse"], response.json())

    # Post /v1/series/fetchseries
    def post_fetch_series(self, *series: "EntityRequest") -> List["SeriesResponse"]:
        """
        Fetch one or more series.
        A timestamp can be specified for each series to conditionally retrieve a result.
        This is typically the value of the metadata LastModifiedTimeStamp from a previous request.
        The result will be in the same order as the request.

        OAuth scope: macrobond_web_api.read_mb

        Codes:
            200 The operation was successful.

            400 The operation failed.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.
        """
        response = self.__session.post_or_raise("v1/series/fetchseries", json=series)
        return cast(List["SeriesResponse"], response.json())

    # Post /fetchseries
    def fetch_series_last_modified_time_stamp(self, *requests: "EntityRequest") -> List["SeriesResponse"]:
        """
        Fetch one or more series.
        A timestamp can be specified for each series to conditionally retrieve a result.
        This is typically the value of the metadata LastModifiedTimeStamp from a previous request.
        The result will be in the same order as the request.

        OAuth scope: macrobond_web_api.read_mb

        Codes:
            200 The operation was successful.

            400 The operation failed.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.
        """
        response = self.__session.post_or_raise("v1/series/fetchseries", json=requests)
        return cast(List["SeriesResponse"], response.json())

    # Get /v1/series/getrevisioninfo
    def get_revision_info(self, *series_names: str) -> List["SeriesWithRevisionsInfoResponse"]:
        """
        Get information about if a record of updates is stored
        for one or more series and the dates of changes.

        OAuth scope: macrobond_web_api.read_mb

        Codes:
            200 The operation was successful.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.
        """
        response = self.__session.get_or_raise("v1/series/getrevisioninfo", params={"n": series_names})
        return cast(List["SeriesWithRevisionsInfoResponse"], response.json())

    # Get /v1/series/fetchvintageseries
    def fetch_vintage_series(
        self, time_of_vintage: datetime, *series_names: str, get_times_of_change: bool = None
    ) -> List["VintageSeriesResponse"]:
        """
        Fetch one or more vintage series.
        The result will be in the same order as the request.

        OAuth scope: macrobond_web_api.read_mb

        Codes:
            200 The operation was successful.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.
        """
        params = {"t": time_of_vintage.isoformat(), "n": series_names}

        if get_times_of_change:
            params["getTimesOfChange"] = "true" if get_times_of_change else "false"

        response = self.__session.get_or_raise("v1/series/fetchvintageseries", params=params)
        return cast(List["VintageSeriesResponse"], response.json())

    # Get /v1/series/fetchallvintageseries
    def get_fetch_all_vintage_series(
        self,
        series_name: str,
        if_modified_since: datetime = None,
        last_revision: datetime = None,
        last_revision_adjustment: datetime = None,
    ) -> List["VintageSeriesResponse"]:
        """
        Fetch all vintage series and the complete history of changes.
        Metadata from the prevision response can be specified to get conditional and
        incremental changes.

        OAuth scope: macrobond_web_api.read_mb

        Codes:

            200 The operation was successful.

            206	The operation was successful, but only new revisions are included.

            304	The series was not modified since the timestamp passed as parmeter ifModifiedSince.

            400 The operation failed.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.

            404 The series could not be found
        """

        params = {"n": series_name}

        if if_modified_since:
            params["ifModifiedSince"] = if_modified_since.isoformat()

        if last_revision:
            params["lastRevision"] = last_revision.isoformat()

        if last_revision_adjustment:
            params["lastRevisionAdjustment"] = last_revision_adjustment.isoformat()

        response = self.__session.get_or_raise(
            "v1/series/fetchallvintageseries",
            params=params,
        )
        return cast(List["VintageSeriesResponse"], response.json())

    # post /v1/series/fetchallvintageseries
    def post_fetch_all_vintage_series(
        self, requests: Sequence["RevisionHistoryRequest"], stream: bool = False
    ) -> "Response":
        return self.__session.post_or_raise("v1/series/fetchallvintageseries", json=requests, stream=stream)

    # Get /v1/series/fetchnthreleaseseries
    def fetch_nth_release_series(
        self, nth: int, *series_names: str, get_times_of_change: bool = None
    ) -> List["SeriesWithTimesOfChangeResponse"]:
        """
        Fetch one or more series where each value is the nth change of the value.
        The result will be in the same order as the request.

        OAuth scope: macrobond_web_api.read_mb

        Codes:
            200 The operation was successful.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.
        """
        params = {
            "n": series_names,
            "nth": nth,
        }

        if get_times_of_change:
            params["getTimesOfChange"] = "true" if get_times_of_change else "false"

        response = self.__session.get_or_raise("v1/series/fetchnthreleaseseries", params=params)
        return cast(List["SeriesWithTimesOfChangeResponse"], response.json())

    # Get /v1/series/fetchobservationhistory
    def fetch_observation_history(
        self, series_name: str, date_of_the_observation: List[datetime]
    ) -> List["SeriesObservationHistoryResponse"]:
        """
        Fetch the history of one or more observations in a time series.
        The result will be in the same order as the request.

        OAuth scope: macrobond_web_api.read_mb

        Codes:
            200 The operation was successful.

            400 The operation failed.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.

            404 The series could not be found
        """
        response = self.__session.get_or_raise(
            "v1/series/fetchobservationhistory",
            params={
                "n": series_name,
                "t": [x.isoformat() for x in date_of_the_observation],
            },
        )
        return cast(List["SeriesObservationHistoryResponse"], response.json())

    # Get /v1/series/getdatapackagelist
    def get_data_package_list(self, if_modified_since: datetime = None) -> "FeedEntitiesResponse":
        """
        Get a list of entities in the subscription list and timestamps when they were last changed.
        You can specify a timestamp to see what has changed since then. For this the
        timeStampForIfModifiedSince in the response from a previous call is typically used.
        This guarantees that you will not miss any updates,
        but you may see the same update more than once.

        OAuth scope: macrobond_web_api.read_mb

        Codes:
            200 The operation was successful.

            401 Unauthorized. Missing, invalid or expired access token.

            403 The account is not set up to use a subscription list.
        """
        params = {}

        if if_modified_since:
            params["ifModifiedSince"] = if_modified_since.isoformat()

        response = self.__session.get_or_raise("v1/series/getdatapackagelist", params=params)
        return cast("FeedEntitiesResponse", response.json())

    # Get /v1/series/entityinfofordisplay
    def entity_info_for_display(self, *entitie_names: str) -> "EntityInfoForDisplayResponse":
        """
        Get formatted information about a time series intended to be displayed to the user

        OAuth scope: macrobond_web_api.read_structure

        Codes:
            200 The operation was successful.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.

            404 The series could not be found.
        """
        response = self.__session.get_or_raise("v1/series/entityinfofordisplay", params={"n": entitie_names})
        return cast("EntityInfoForDisplayResponse", response.json())

    # Post /v1/series/fetchunifiedseries
    def fetch_unified_series(self, request: "UnifiedSeriesRequest") -> "UnifiedSeriesResponse":
        """
        Fetch one or more series and convert them to a common frequency,
        calendar and optionally a common currency.
        Specify properties for frequency conversion and method to fill in missing values.
        The resulting list of series will be in the same order as in the request.

        OAuth scope: macrobond_web_api.read_mb

        Codes:
            200 The operation was successful.

            400 The operation failed.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.
        """
        response = self.__session.post_or_raise("v1/series/fetchunifiedseries", json=request)
        return cast("UnifiedSeriesResponse", response.json())
