from typing import List, Union, cast, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session
    from .series_tree import (
        SeriesTreeNodeLeaf,
        SeriesTreeNodeBranchRef,
        SeriesTreeNodeBranch,
        SeriesTreeListingResponse,
        SeriesTreeLocationPart,
    )


class SeriesTreeMethods:
    """Operations related to the visual series database tree structure"""

    def __init__(self, session: "Session") -> None:
        self.__session = session

    def get_nodes(
        self, path: str = None, filter_path: str = None
    ) -> List[Union["SeriesTreeNodeLeaf", "SeriesTreeNodeBranchRef", "SeriesTreeNodeBranch"]]:
        """
        Get the nodes of a branch of the series database tree.

        OAuth scope: macrobond_web_api.read_structure

        Codes:
            200 The operation was successful.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.
        """
        response = self.__session.get_or_raise(
            "v1/seriestree/getnodes", params={"path": path, "filterPath": filter_path}
        )
        return cast(
            List[
                Union[
                    "SeriesTreeNodeLeaf",
                    "SeriesTreeNodeBranchRef",
                    "SeriesTreeNodeBranch",
                ]
            ],
            response.json(),
        )

    def get_leaf_series(self, path: str, *dp: str) -> "SeriesTreeListingResponse":
        """
        Get a structured list of series for a leaf in the
        database tree identified by the path of the tree branches.

        OAuth scope: macrobond_web_api.read_structure

        Codes:
            200 The operation was successful.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.

            404 The path was not found.
        """
        response = self.__session.get_or_raise("v1/seriestree/getleafseries", params={"path": path, "dp": dp})
        return cast("SeriesTreeListingResponse", response.json())

    def find_locations(self, series_name: str) -> List["SeriesTreeLocationPart"]:
        """
        Find the locations where this series can be found in the database tree.

        OAuth scope: macrobond_web_api.read_structure

        Codes:
            200 The operation was successful.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.
        """
        response = self.__session.get_or_raise("v1/seriestree/findlocations", params={"seriesName": series_name})
        return cast(List["SeriesTreeLocationPart"], response.json())
