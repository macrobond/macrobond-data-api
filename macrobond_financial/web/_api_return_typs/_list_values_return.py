# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import List, TYPE_CHECKING

from macrobond_financial.common._get_pandas import _get_pandas

from macrobond_financial.common.api_return_typs import ListValuesReturn

from macrobond_financial.common.typs import (
    MetadataValueInformation,
    MetadataValueInformationItem,
)

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore
    from ..session import Session

    from macrobond_financial.common.typs import TypedDictMetadataValueInformation

    from ..web_typs import (
        MetadataValueInformationItem as WebMetadataValueInformationItem,
    )


class _ListValuesReturn(ListValuesReturn):
    def __init__(self, session: "Session", name: str) -> None:
        super().__init__()
        self.__session = session
        self.__name = name

    def object(self) -> MetadataValueInformation:
        values = self.__session.metadata.list_attribute_values(self.__name)
        return MetadataValueInformation(
            self.__name,
            tuple(
                map(
                    lambda x: MetadataValueInformationItem(
                        x["value"], x["description"], x.get("comment")
                    ),
                    values,
                )
            ),
        )

    def list_of_dicts(self) -> List["TypedDictMetadataValueInformation"]:
        values = self.__session.metadata.list_attribute_values(self.__name)

        def to_dict(
            info: "WebMetadataValueInformationItem",
        ) -> "TypedDictMetadataValueInformation":
            return {
                "attribute_name": self.__name,
                "value": info["value"],
                "description": info["description"],
                "comment": info.get("comment"),
            }

        return list(map(to_dict, values))

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.list_of_dicts()
        return pandas.DataFrame(*args, **kwargs)
