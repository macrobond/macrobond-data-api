from typing import List, cast, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session
    from .series_storage_location_response import SeriesStorageLocationResponse
    from .series_request import SeriesRequest


class InHouseSeriesMethods:
    """Additional operations for in-house series"""

    def __init__(self, session: "Session") -> None:
        self.__session = session

    # DELETE /v1/series/deleteseries
    def delete_series(self, entitie_name: str) -> None:
        """
        Delete an in-house time series.
        The name typically starts with 'ih:mb:'.

        OAuth scope: macrobond_web_api.write_ih

        Codes:
            200	The operation was successful.

            400	The operation failed.

            401	Unauthorized. Missing, invalid or expired access token.

            403	Forbidden. Not authorized.

            404	The series could not be found.
        """
        self.__session.delete_or_raise("v1/series/deleteseries", params={"n": entitie_name})

    # Post /v1/series/uploadseries
    def upload_series(self, seriesRequest: "SeriesRequest") -> None:
        """
        Upload an in-house time series.
        In the metadata, PrimName, Frequency, IHCategory, Region and Description must be set.
        If no vector of dates is specified, the StartDate must be includeded in the metadata.
        For daily series, DayMask must also be included.

        OAuth scope: macrobond_web_api.write_ih

        Codes:
            200 The operation was successful.

            400 The operation failed.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.
        """
        self.__session.post_or_raise("v1/series/uploadseries", json=seriesRequest)

    # Get /v1/seriestree/getseriesstoragelocations
    def get_series_storage_locations(self) -> List["SeriesStorageLocationResponse"]:
        """
        Get a list of locations where in-house series can be stored.

        OAuth scope: macrobond_web_api.read_structure and macrobond_web_api.write_ih

        Codes:
            200 The operation was successful.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.
        """
        response = self.__session.get_or_raise("v1/seriestree/getseriesstoragelocations")
        return cast(List["SeriesStorageLocationResponse"], response.json())

    # Get /v1/seriestree/getusedinhousecategories
    def get_used_inhouse_categories(self) -> List[str]:
        """
        Get a list of values of the IHCategory attribute that has previously been used.
        This can be used to suggest values to the user when creating in-house series.

        OAuth scope: macrobond_web_api.read_structure and macrobond_web_api.write_ih

        Codes:
            200 The operation was successful.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.
        """
        response = self.__session.get_or_raise("v1/seriestree/getusedinhousecategories")
        return cast(List[str], response.json())
