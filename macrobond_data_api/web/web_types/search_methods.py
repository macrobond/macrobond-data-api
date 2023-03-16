from typing import cast, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session
    from .search import (
        SearchResponse,
        SearchRequest,
        SearchForDisplayResponse,
        SearchForDisplayRequest,
        ItemListingResponse,
    )


class SearchMethods:
    """Search for time series and other entites"""

    def __init__(self, session: "Session") -> None:
        self.__session = session

    # get /entities
    def get_entities(
        self,
        entity_type: List[str] = None,
        text: str = None,
        include_discontinued: bool = None,
        _filter: Dict[str, str] = None,
        no_meta_data: bool = None,
        allow_long_result: bool = None,
    ) -> "SearchResponse":
        """
        Search for time series and other entites matching attribute values.
        If the same attribute name is specified more than once,
        then entities matching any of them will be included. If the value is *,
        any value will match. If ! is specified before an attribute name,
        entities matching the value will be excluded instead of included.

        OAuth scope: macrobond_web_api.search_mb

        Codes:
            200 The operation was successful.

            400 Request failed.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.

            404 At least one attribute was not found.
        """

        params = {
            "entityType": entity_type,
            "text": text,
            "filter": _filter,
        }

        if no_meta_data:
            params["noMetaData"] = "true" if no_meta_data else "false"

        if include_discontinued:
            params["includeDiscontinued"] = "true" if include_discontinued else "false"

        if allow_long_result:
            params["allowLongResult"] = "true" if allow_long_result else "false"

        response = self.__session.get_or_raise("v1/search/entities", params=params)

        return cast("SearchResponse", response.json())

    # post /entities
    def post_entities(self, request: "SearchRequest") -> "SearchResponse":
        """
        Search for time series and other entites matching attribute values.

        OAuth scope: macrobond_web_api.search_mb

        Codes:
            200 The operation was successful.

            400 Request failed.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.

            404 At least one attribute was not found.
        """
        response = self.__session.post_or_raise("v1/search/entities", json=request)
        return cast("SearchResponse", response.json())

    def filter_lists(self, entity_type: str) -> List["ItemListingResponse"]:
        """
        Get a structured list of all saved filter lists of the specified type.

        OAuth scope: macrobond_web_api.read_structure or macrobond_web_api.search_mb

        Codes:
            200 The operation was successful.

            400 Request failed.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.
        """
        response = self.__session.get_or_raise("v1/search/filterlists", params={"entityType": entity_type})
        return cast(List["ItemListingResponse"], response.json())

    def entities_for_display(self, request: "SearchForDisplayRequest") -> "SearchForDisplayResponse":
        """
        Search for time series and other entites matching attribute values and return the
        selected metadata formatted for presentation purposes.

        OAuth scope: macrobond_web_api.read_structure

        Codes:
            200 The operation was successful.

            400 Request failed.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.

            404 At least one attribute was not found.
        """
        response = self.__session.post_or_raise("v1/search/entitiesfordisplay", json=request)
        return cast("SearchForDisplayResponse", response.json())
