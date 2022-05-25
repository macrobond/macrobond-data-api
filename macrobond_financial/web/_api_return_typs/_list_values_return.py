# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import TYPE_CHECKING

from macrobond_financial.common.api_return_types import ListValuesReturn

from macrobond_financial.common.types import (
    MetadataValueInformation,
    MetadataValueInformationItem,
)

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session


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
                        self.__name, x["value"], x["description"], x.get("comment")
                    ),
                    values,
                )
            ),
        )
