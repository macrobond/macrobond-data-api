# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import List
from typing_extensions import TypedDict


class EntityNameWithTimeStamp(TypedDict):
    """Name and timestamp of an entity"""

    name: str
    """The entity name"""

    modified: str
    """Timestamp when this entity was last modified"""


class FeedEntitiesResponse(TypedDict):
    """List of entities available in a feed"""

    timeStampForIfModifiedSince: str
    """
    A timestamp to pass as the ifModifiedSince parameter
    in the next request to get incremental updates.
    """

    truncated: bool
    """
    Indicates if the list of entities is complete.
    If the list of feedable items is too long, all entities will not be included.
    """

    entities: List["EntityNameWithTimeStamp"]
    """A list of entity names and timestamps when they were last modified."""
