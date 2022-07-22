# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING, Any, Dict, Iterator, MutableMapping

if TYPE_CHECKING:  # pragma: no cover
    from ._metadata_directory import _MetadataTypeDirectory


class _Metadata(MutableMapping[str, Any]):
    __slots__ = ("__type_directory", "__data")

    def __init__(self, data: Dict[str, Any], type_directory: "_MetadataTypeDirectory") -> None:
        self.__data = data
        self.__type_directory = type_directory

    def __getitem__(self, key: str) -> Any:
        if key == "Name":
            return self.__data[key]
        return self.__type_directory.convert(key, self.__data[key])

    def __setitem__(self, key: str, val) -> None:
        self.__data[key] = val

    def __delitem__(self, key: str) -> None:
        self.__data.__delitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.__data.__iter__()

    def __len__(self) -> int:
        return self.__data.__len__()

    def __repr__(self):
        return dict(self.items()).__repr__()
