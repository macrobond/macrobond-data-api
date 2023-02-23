from typing import Any, TYPE_CHECKING, Sequence
from datetime import datetime, timezone


try:
    from pywintypes import TimeType
except ImportError as ex:
    ...

if TYPE_CHECKING:  # pragma: no cover
    from .com_types import Entity as ComEntity
    from macrobond_data_api.common.types.metadata import Metadata


def _get_val(name: str, values: Sequence[Any]) -> Any:
    if isinstance(values[0], TimeType):
        if name == "LastModifiedTimeStamp":
            datetime_ = values[0]
            return datetime(
                datetime_.year,
                datetime_.month,
                datetime_.day,
                datetime_.hour,
                datetime_.minute,
                datetime_.second,
                datetime_.microsecond,
                tzinfo=datetime.now().astimezone().tzinfo,
            ).astimezone(timezone.utc)
        if name in ("LastRevisionAdjustmentTimeStamp", "LastRevisionTimeStamp"):
            datetime_ = values[0]
            return datetime(
                datetime_.year,
                datetime_.month,
                datetime_.day,
                datetime_.hour,
                datetime_.minute,
                datetime_.second,
                datetime_.microsecond,
                tzinfo=timezone.utc,
            )
        values = [
            datetime(x.year, x.month, x.day, x.hour, x.minute, x.second, x.microsecond, timezone.utc) for x in values
        ]
        return values[0] if len(values) == 1 else values
    return values[0] if len(values) == 1 else list(values)


def _fill_metadata_from_entity(com_entity: "ComEntity") -> "Metadata":
    metadata = com_entity.Metadata
    ret = {x: _get_val(x, metadata.GetValues(x)) for x, _ in metadata.ListNames()}
    # ret = {x: metadata.GetValues(x) for x in (x[0] for x in metadata.ListNames())}
    ret.setdefault("FullDescription", com_entity.Title)

    return ret
