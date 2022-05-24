# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING


from macrobond_financial.common.api_return_typs import ListValuesReturn

from macrobond_financial.common.types import (
    MetadataValueInformation,
    MetadataValueInformationItem,
)


if TYPE_CHECKING:  # pragma: no cover
    from ..com_typs import Database


class _ListValuesReturn(ListValuesReturn):
    def __init__(self, database: "Database", name: str) -> None:
        self._database = database
        self._name = name

    def object(self) -> MetadataValueInformation:
        info = self._database.GetMetadataInformation(self._name)
        values = info.ListAllValues()

        return MetadataValueInformation(
            self._name,
            tuple(
                map(
                    lambda x: MetadataValueInformationItem(
                        self._name, x.Value, x.Description, x.Comment
                    ),
                    values,
                )
            ),
        )
