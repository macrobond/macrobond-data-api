from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING, Literal, List, Sequence

from macrobond_data_api.common.enums import StatusCode

from .entity import Entity, EntityColumnsLiterals

from .release_event import ReleaseEvent

if TYPE_CHECKING:  # pragma: no cover
    from .metadata import Metadata

ReleaseColumnsLiterals = Literal[EntityColumnsLiterals, "Events"]

ReleaseColumns = List[ReleaseColumnsLiterals]

__pdoc__ = {
    "Release.__init__": False,
}


@dataclass(init=False)
class Release(Entity):
    """
    Represents a Macrobond release entity.
    """

    __slots__ = ("events",)

    events: Optional[Sequence[ReleaseEvent]]

    def __init__(
        self,
        name: str,
        error_message: Optional[str],
        status_code: StatusCode,
        metadata: Optional["Metadata"],
        events: Optional[Sequence[ReleaseEvent]],
    ) -> None:
        super().__init__(name, error_message, status_code, metadata)

        self.events = events
        """The schedule of the release or not specified if the schedule is not known of if there was an error"""
