from typing import Optional, TypedDict


class EntityRequest(TypedDict, total=False):
    """Request of an entity and an optional timestamp of last modification"""

    name: str
    """The name of the entity"""

    ifModifiedSince: Optional[str]
    """
    If specified, the enitity will only be returned if modified since the specified time.
    If not, the ErrorCode field of the response will be NotModified (304).
    """
