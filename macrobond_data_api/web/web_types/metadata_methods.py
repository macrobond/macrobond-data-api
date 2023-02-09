from typing import List, cast, Tuple, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session
    from .metadata import MetadataAttributeInformationResponse, MetadataValueInformationResponse


class MetadataMethods:
    """Metadata operations"""

    def __init__(self, session: "Session") -> None:
        self.__session = session

    # Get /v1/metadata/getattributeinformation
    def get_attribute_information(self, *attribute_names: str) -> List["MetadataAttributeInformationResponse"]:
        """
        Get information about metadata attributes.
        The result will be in the same order as the request.

        OAuth scope: macrobond_web_api.read_mb

        Codes:
            200 The operation was successful.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.

            404 At least one attribute was not found.

        """
        response = self.__session.get_or_raise("v1/metadata/getattributeinformation", params={"n": attribute_names})
        return cast(List["MetadataAttributeInformationResponse"], response.json())

    # Get /v1/metadata/getvalueinformation
    def get_value_information(self, *metadata_value: Tuple[str, str]) -> "MetadataValueInformationResponse":
        """
        Get information about metadata values.
        The result will be in the same order as the request.

        OAuth scope: macrobond_web_api.read_mb

        Codes:
            200 The operation was successful.

            400 Malformed request.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.

            404 At least one attribute or value was not found.
        """
        response = self.__session.get_or_raise(
            "v1/metadata/getvalueinformation",
            params={"v": list(map(lambda x: x[0] + "," + x[1], metadata_value))},
        )
        return cast("MetadataValueInformationResponse", response.json())

    # Get /v1/metadata/listattributevalues
    def list_attribute_values(self, attribute_name: str) -> "MetadataValueInformationResponse":
        """
        List all metadata attribute values.
        The attribute must have the property canListValues.

        OAuth scope: macrobond_web_api.read_mb

        Codes:
            200 The operation was successful.

            400 Values cannot be listed for the attribute.

            401 Unauthorized. Missing, invalid or expired access token.

            403 Forbidden. Not authorized.

            404 The attribute was not found.
        """
        response = self.__session.get_or_raise("v1/metadata/listattributevalues", params={"n": attribute_name})
        return cast("MetadataValueInformationResponse", response.json())
