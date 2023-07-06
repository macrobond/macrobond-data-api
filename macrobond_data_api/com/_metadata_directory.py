from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:  # pragma: no cover
    from .com_types.connection import Connection


class _MetadataType:
    __slots__ = ("can_have_multiple_values",)

    can_have_multiple_values: bool

    def __init__(self, can_have_multiple_values: bool) -> None:
        super().__init__()
        self.can_have_multiple_values = can_have_multiple_values


class _MetadataTypeDirectory:
    __slots__ = ("connection",)

    connection: Optional["Connection"]

    _type_db: Dict[str, Optional[_MetadataType]] = {}

    def __init__(self, connection: Optional["Connection"]) -> None:
        super().__init__()
        self.connection = connection

    def convert(self, attribute_name: str, obj: Any) -> Any:
        type_info = _MetadataTypeDirectory._type_db.get(attribute_name)

        if type_info is None and self.connection is not None:
            try:
                info = self.connection.Database.GetMetadataInformation(attribute_name)
                type_info = _MetadataTypeDirectory._type_db[attribute_name] = _MetadataType(info.CanHaveMultipleValues)
            except Exception as ex:  # pylint: disable=W0703
                if len(ex.args) >= 3 and len(ex.args[2]) >= 3 and ex.args[2][2].startswith("Unknown metadata name: "):
                    _MetadataTypeDirectory._type_db[attribute_name] = None
                else:
                    raise ex

        if type_info is not None:
            if type_info.can_have_multiple_values and not isinstance(obj, list):
                return [obj]

        return obj

    def close(self) -> None:
        self.connection = None
