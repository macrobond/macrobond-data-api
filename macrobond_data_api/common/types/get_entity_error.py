from typing import List, Optional, Tuple, Iterable
from dataclasses import dataclass

__pdoc__ = {
    "EntitieErrorInfo.__init__": False,
    "GetEntitiesError.__init__": False,
}


@dataclass(init=False)
class EntityErrorInfo:
    """
    Represents a failed entity retrieval.
    """

    __slots__ = ("name", "error_message")

    name: str
    error_message: str

    @property
    def is_error(self) -> bool:
        """
        Always returns True since this instance always indicates an error.
        """
        return True

    def __init__(self, name: str, error_message: str):
        self.name = name
        """The name of the entity."""

        self.error_message = error_message
        """Contains the error message."""


@dataclass(init=False)
class GetEntitiesError(Exception):
    entities: List[EntityErrorInfo]
    message: str

    def __init__(self, entities: List[EntityErrorInfo]):
        self.entities = entities
        """entities"""

        self.message = "failed to retrieve:\n" + (
            "\n".join("\t" + x.name + " error_message: " + x.error_message for x in self.entities)
        )
        """message"""

        super().__init__(self.message)

    @classmethod
    def _raise_if(cls, entities: Iterable[Tuple[str, Optional[str]]]) -> None:
        entities_list = [EntityErrorInfo(x, y) for x, y in entities if y]
        if entities_list:
            raise GetEntitiesError(entities_list)
