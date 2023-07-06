from typing import TYPE_CHECKING, Any, Dict, Iterator

from macrobond_data_api.common.types.metadata import Metadata

if TYPE_CHECKING:  # pragma: no cover
    from ._metadata_directory import _MetadataTypeDirectory


class _Metadata(Metadata):
    __slots__ = ("__data", "__type_directory")

    def __init__(self, data: Dict[str, Any], type_directory: "_MetadataTypeDirectory") -> None:
        self.__data = data
        self.__type_directory = type_directory

    def __getitem__(self, key: str) -> Any:
        if key == "Name":
            return self.__data[key]
        return self.__type_directory.convert(key, self.__data[key])

    def __setitem__(self, key: str, val: Any) -> None:
        self.__data[key] = val

    def __delitem__(self, key: str) -> None:
        self.__data.__delitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.__data.__iter__()

    def __len__(self) -> int:
        return self.__data.__len__()

    def __repr__(self) -> str:
        return dict(self.items()).__repr__()
