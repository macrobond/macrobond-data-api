from typing import Any, Dict, TYPE_CHECKING, Sequence
from datetime import datetime, timezone

try:
    from pywintypes import TimeType
except ImportError as ex:
    ...

if TYPE_CHECKING:  # pragma: no cover
    from .com_types import Entity as ComEntity


def _fill_metadata_from_entity(com_entity: "ComEntity") -> Dict[str, Any]:
    def get_val(values: Sequence[Any]) -> Any:
        if isinstance(values[0], TimeType):
            values = [
                datetime(x.year, x.month, x.day, x.hour, x.minute, x.second, x.microsecond, timezone.utc)
                for x in values
            ]
        return values[0] if len(values) == 1 else values

    metadata = com_entity.Metadata
    ret = {x: get_val(metadata.GetValues(x)) for x in (x[0] for x in metadata.ListNames())}

    ret.setdefault("FullDescription", com_entity.Title)

    return ret
