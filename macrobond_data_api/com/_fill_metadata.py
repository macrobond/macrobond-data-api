from typing import Any, TYPE_CHECKING, Sequence
from datetime import datetime, timezone

from ._metadata import _Metadata

try:
    from pywintypes import TimeType
except ImportError as ex:
    ...

if TYPE_CHECKING:  # pragma: no cover
    from .com_api import ComApi
    from .com_types import Entity as ComEntity
    from .com_types import Series as ComSeries
    from .com_types import Metadata as ComMetadata
    from macrobond_data_api.common.types.values_metadata import ValuesMetadata


def _get_val_old(name: str, values: Sequence[Any]) -> Any:
    if isinstance(values[0], TimeType):
        if name in ("OriginalStartDate", "OriginalEndDate"):
            datetime_ = values[0]
            return datetime(
                datetime_.year,
                datetime_.month,
                datetime_.day,
                datetime_.hour,
                datetime_.minute,
                datetime_.second,
                datetime_.microsecond,
            )
        if name in ("LastModifiedTimeStamp"):
            datetime_ = values[0]
            return datetime(
                datetime_.year,
                datetime_.month,
                datetime_.day,
                datetime_.hour,
                datetime_.minute,
                datetime_.second,
                datetime_.microsecond,
            ).astimezone(timezone.utc)
        values = [
            datetime(x.year, x.month, x.day, x.hour, x.minute, x.second, x.microsecond, timezone.utc) for x in values
        ]
        return values[0] if len(values) == 1 else values
    return values[0] if len(values) == 1 else list(values)


def _get_val_new(name: str, values: Sequence[Any]) -> Any:
    if isinstance(values[0], TimeType):
        if name in ("OriginalEndDate", "OriginalStartDate"):
            return datetime(values[0].year, values[0].month, values[0].day)
        values = [
            datetime(x.year, x.month, x.day, x.hour, x.minute, x.second, x.microsecond).astimezone(timezone.utc)
            for x in values
        ]
        return values[0] if len(values) == 1 else values
    return values[0] if len(values) == 1 else list(values)


def _fill_metadata_from_metadata(
    com_metadata: "ComMetadata", api: "ComApi", add_empty_revision_time_stamp: bool = False
) -> _Metadata:
    if api._old_metadata_handling:
        metadata = _Metadata(
            {x: _get_val_old(x, com_metadata.GetValues(x)) for x, _ in com_metadata.ListNames()},
            api._metadata_type_directory,
        )
    else:
        metadata = _Metadata(
            {x: _get_val_new(x, com_metadata.GetValues(x)) for x, _ in com_metadata.ListNames()},
            api._metadata_type_directory,
        )

    if add_empty_revision_time_stamp and "RevisionTimeStamp" not in metadata:
        metadata["RevisionTimeStamp"] = None
    return metadata


def _fill_metadata_from_entity(com_entity: "ComEntity", api: "ComApi") -> _Metadata:
    ret = _fill_metadata_from_metadata(com_entity.Metadata, api)
    if "FullDescription" not in ret:
        ret["FullDescription"] = com_entity.Title
    return ret


def _fill_values_metadata_from_series(
    com_series: "ComSeries", api: "ComApi", add_empty_revision_time_stamp: bool = False
) -> "ValuesMetadata":
    return [_fill_metadata_from_metadata(x, api, add_empty_revision_time_stamp) for x in com_series.ValuesMetadata]
