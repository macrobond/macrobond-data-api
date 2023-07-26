from typing import Optional, Any, List, TypedDict


class MetadataValueInformationItem(TypedDict, total=False):
    """Information about a metadata value"""

    attributeName: str
    """The name of the metadata attribute"""

    value: Any
    """The value"""

    description: str
    """The description of the metadata value"""

    comment: Optional[str]
    """The comment of the metadata value"""


MetadataValueInformationResponse = List[MetadataValueInformationItem]
