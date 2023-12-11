import time
from typing import TYPE_CHECKING, Any, Dict, Optional
from datetime import datetime, timedelta, timezone

try:
    from pywintypes import TimeType
except ImportError as ex_:
    pass

if TYPE_CHECKING:  # pragma: no cover
    from .com_types.connection import Connection
    from .com_types.metadata_information import MetadataInformation, RestrictionLiteral
    from .com_types import Metadata as ComMetadata


class _MetadataType:
    __slots__ = ("can_have_multiple_values", "restriction")

    can_have_multiple_values: bool
    restriction: Optional["RestrictionLiteral"]

    def __init__(self, info: "MetadataInformation") -> None:
        super().__init__()
        self.can_have_multiple_values = info.CanHaveMultipleValues
        self.restriction = info.Restriction


def _convert_datetime_as_astimezone_utc(dt: datetime) -> datetime:
    if dt.year > 1970:
        return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond).astimezone(
            timezone.utc
        )
    delta = time.altzone if time.daylight != 0 else time.timezone
    return datetime(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, tzinfo=timezone.utc
    ) + timedelta(seconds=delta)


class _MetadataTypeDirectory:
    __slots__ = ("connection", "old_metadata_handling")

    connection: Optional["Connection"]
    old_metadata_handling: bool

    _type_db: Dict[str, Optional[_MetadataType]] = {}

    def __init__(self, connection: Optional["Connection"], old_metadata_handling: bool) -> None:
        super().__init__()
        self.connection = connection
        self.old_metadata_handling = old_metadata_handling

    def fill_metadata_from_metadata(
        self, com_metadata: "ComMetadata", add_empty_revision_time_stamp: bool = False
    ) -> Dict[str, Any]:
        metadata = {x: self._convert(x, com_metadata.GetValues(x)) for x, _ in com_metadata.ListNames()}

        if add_empty_revision_time_stamp and "RevisionTimeStamp" not in metadata:
            metadata["RevisionTimeStamp"] = None
        return metadata

    def _convert(self, name: str, obj: Any) -> Any:
        type_info = _MetadataTypeDirectory._type_db.get(name)

        if type_info is None and self.connection is not None:
            try:
                info = self.connection.Database.GetMetadataInformation(name)
                type_info = _MetadataTypeDirectory._type_db[name] = _MetadataType(info)
            except Exception as ex:  # pylint: disable=W0703
                if len(ex.args) >= 3 and len(ex.args[2]) >= 3 and ex.args[2][2].startswith("Unknown metadata name: "):
                    _MetadataTypeDirectory._type_db[name] = None
                else:
                    raise ex

        if self.old_metadata_handling:
            return self._old_metadata_handling(name, obj, type_info)

        if type_info:
            return self._convert_with_type_info(obj, type_info)

        # fall back if no type_info
        if isinstance(obj[0], TimeType):
            obj = [_convert_datetime_as_astimezone_utc(x) for x in obj]
            return obj[0] if len(obj) == 1 else obj
        return obj[0] if len(obj) == 1 else list(obj)

    # this will be removed when we drop support for old metadata handling
    def _old_metadata_handling(self, name: str, obj: Any, type_info: Optional[_MetadataType]) -> Any:
        if isinstance(obj[0], TimeType):
            if name in ("OriginalStartDate", "OriginalEndDate"):
                dt = obj[0]
                return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
            if name in ("LastModifiedTimeStamp"):
                return _convert_datetime_as_astimezone_utc(obj[0])
            obj = [
                datetime(x.year, x.month, x.day, x.hour, x.minute, x.second, x.microsecond, timezone.utc) for x in obj
            ]
            obj = obj[0] if len(obj) == 1 else obj
        else:
            obj = obj[0] if len(obj) == 1 else list(obj)

        if type_info is not None:
            if type_info.can_have_multiple_values and not isinstance(obj, list):
                return [obj]
        return obj

    def _convert_with_type_info(self, obj: Any, type_info: _MetadataType) -> Any:
        if isinstance(obj[0], TimeType):
            if type_info.restriction == "date":
                if type_info.can_have_multiple_values:
                    return [datetime(x.year, x.month, x.day) for x in obj]
                return datetime(obj[0].year, obj[0].month, obj[0].day)
            if type_info.can_have_multiple_values:
                return [_convert_datetime_as_astimezone_utc(x) for x in obj]
            return _convert_datetime_as_astimezone_utc(obj[0])
        if type_info.can_have_multiple_values:
            return list(obj)
        return obj[0]

    def close(self) -> None:
        self.connection = None
