# -*- coding: utf-8 -*-

from typing import List, TYPE_CHECKING

from macrobond_financial.common._get_pandas import _get_pandas

from macrobond_financial.common.api_return_typs import ListValuesReturn

from macrobond_financial.common.typs import (
    MetadataValueInformation,
    MetadataValueInformationItem,
)


if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore
    from ..com_typs import (
        Database,
        MetadataValueInformation as ComMetadataValueInformation,
    )

    from macrobond_financial.common.typs import TypedDictMetadataValueInformation


class _ListValuesReturn(ListValuesReturn):
    def __init__(self, database: "Database", name: str) -> None:
        super().__init__()
        self.__database = database
        self.__name = name

    def object(self) -> MetadataValueInformation:
        info = self.__database.GetMetadataInformation(self.__name)
        values = info.ListAllValues()

        return MetadataValueInformation(
            self.__name,
            tuple(
                map(
                    lambda x: MetadataValueInformationItem(
                        x.Value, x.Description, x.Comment
                    ),
                    values,
                )
            ),
        )

    def list_of_dicts(self) -> List["TypedDictMetadataValueInformation"]:
        info = self.__database.GetMetadataInformation(self.__name)
        values = info.ListAllValues()

        def to_dict(
            info: "ComMetadataValueInformation",
        ) -> "TypedDictMetadataValueInformation":
            return {
                "attribute_name": self.__name,
                "value": info.Value,
                "description": info.Description,
                "comment": info.Comment,
            }

        return list(map(to_dict, values))

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.list_of_dicts()
        return pandas.DataFrame(*args, **kwargs)
