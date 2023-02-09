from datetime import datetime


class SubscriptionListItem:
    __slots__ = ("name", "modified")

    name: str
    """The entity name"""

    modified: datetime
    """Timestamp when this entity was last modified"""

    def __init__(self, name: str, modified: datetime) -> None:
        self.name = name
        self.modified = modified

    def __eq__(self, other):
        return self is other or (
            isinstance(other, SubscriptionListItem) and self.name == other.name and self.modified == other.modified
        )

    def __repr__(self):
        return f"SubscriptionListItem name: {self.name}, modified: {self.modified}"
