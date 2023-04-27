from datetime import datetime
from dataclasses import dataclass


@dataclass(init=False)
class DataPackageListItem:
    __slots__ = ("name", "modified")

    name: str
    modified: datetime

    def __init__(self, name: str, modified: datetime) -> None:
        self.name = name
        """The entity name"""

        self.modified = modified
        """Timestamp when this entity was last modified"""
