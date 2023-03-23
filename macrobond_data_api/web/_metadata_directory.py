from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, Optional

from json import load as json_load

from macrobond_data_api.common.types._parse_iso8601 import _parse_iso8601

from ..common.enums import MetadataAttributeType
from .web_types.metadata import MetadataAttributeTypeRestriction

from .session import ProblemDetailsException

if TYPE_CHECKING:  # pragma: no cover
    from .session import Session


class _MetadataType:
    __slots__ = ("value_type", "value_restriction")

    def __init__(
        self,
        value_type: MetadataAttributeType,
        value_restriction: Optional[MetadataAttributeTypeRestriction],
    ) -> None:
        super().__init__()
        self.value_type = value_type
        self.value_restriction = value_restriction


class _MetadataTypeDirectory:
    __slots__ = ("session",)

    session: Optional["Session"]

    _type_db: Dict[str, Optional[_MetadataType]] = {}

    def __init__(self, session: Optional["Session"]) -> None:
        super().__init__()
        self.session = session

    def convert(self, attribute_name: str, obj: Any) -> Any:
        type_info = _MetadataTypeDirectory._type_db.get(attribute_name)

        if type_info is None and self.session is not None:
            try:
                info = self.session.metadata.get_attribute_information(attribute_name)[0]
                type_info = _MetadataTypeDirectory._type_db[attribute_name] = _MetadataType(
                    info["valueType"], info.get("valueRestriction")
                )
            except ProblemDetailsException as ex:
                if ex.status == 404:
                    _MetadataTypeDirectory._type_db[attribute_name] = None
                else:
                    raise ex

        if type_info is not None:
            if type_info.value_type == MetadataAttributeType.INT:
                return int(obj)
            if type_info.value_type == MetadataAttributeType.DOUBLE:
                return float(obj)
            if type_info.value_type == MetadataAttributeType.TIME_STAMP:
                if type_info.value_restriction == MetadataAttributeTypeRestriction.DATE:
                    return datetime(int(obj[0:4]), int(obj[5:7]), int(obj[8:10]))
                time = _parse_iso8601(obj)
                if time.tzinfo == timezone.utc:
                    time = datetime(
                        time.year,
                        time.month,
                        time.day,
                        time.hour,
                        time.minute,
                        time.second,
                        time.microsecond,
                        tzinfo=timezone.utc,
                    )
                return time
            if (
                type_info.value_type == MetadataAttributeType.STRING
                and type_info.value_restriction == MetadataAttributeTypeRestriction.JSON
            ):
                return json_load(obj)
        return obj

    def close(self) -> None:
        self.session = None
