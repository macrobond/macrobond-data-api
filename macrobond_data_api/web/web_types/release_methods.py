from datetime import datetime

from typing import Any, cast, TYPE_CHECKING, List, Optional, Dict

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session
    from .release_entity_response import ReleaseEntityResponse


class ReleaseMethods:
    """Lists upcoming releases for given release name"""

    def __init__(self, session: "Session") -> None:
        self.__session = session

    # get /v1/release/upcomingreleases
    def get_upcomingreleases(
        self,
        *releases: str,
        end_time: Optional[datetime] = None,
    ) -> List["ReleaseEntityResponse"]:
        """
        List upcoming releases until provided cutoff time

        OAuth scope: macrobond_web_api.read_mb

        OAuth scope: macrobond_web_api.search_mb

        Codes:
            200 The operation was successful.

            400 The requested entity was not a Release entity

            401	Unauthorized. Missing, invalid or expired access token.

            403	Forbidden. Not authorized.

            404	The entity was not found

            429	Too many requests. The maximum number of requests per day has been reached.
        """

        params: Dict[str, Any] = {"n": releases}
        if end_time:
            params["endTime"] = end_time.isoformat()

        response = self.__session.get_or_raise("v1/release/upcomingreleases", params=params)

        return cast(List["ReleaseEntityResponse"], response.json())

    # post /upcomingreleases
    def post_upcomingreleases(
        self,
        *releases: str,
        end_time: Optional[datetime] = None,
    ) -> List["ReleaseEntityResponse"]:
        """
        List upcoming releases until provided cutoff time

        OAuth scope: macrobond_web_api.read_mb

        OAuth scope: macrobond_web_api.search_mb

        Codes:
            200 The operation was successful.

            400 The requested entity was not a Release entity

            401	Unauthorized. Missing, invalid or expired access token.

            403	Forbidden. Not authorized.

            404	The entity was not found

            429	Too many requests. The maximum number of requests per day has been reached.
        """

        params: Dict[str, Any] = {}
        if end_time:
            params["endTime"] = end_time.isoformat()

        response = self.__session.post_or_raise("v1/release/upcomingreleases", params=params, json=releases)
        return cast(List["ReleaseEntityResponse"], response.json())
