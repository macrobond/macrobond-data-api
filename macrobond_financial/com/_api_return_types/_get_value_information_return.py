# -*- coding: utf-8 -*-

from typing import List, TYPE_CHECKING, Tuple

from macrobond_financial.common.api_return_typs import GetValueInformationReturn

from macrobond_financial.common.types import MetadataValueInformationItem


if TYPE_CHECKING:  # pragma: no cover
    from ..com_typs import Database


def is_error_with_text(ex: Exception, text: str) -> bool:
    return len(ex.args) >= 3 and len(ex.args[2]) >= 3 and ex.args[2][2].startswith(text)


class _GetValueInformationReturn(GetValueInformationReturn):
    def __init__(
        self, database: "Database", name_val: Tuple[Tuple[str, str], ...]
    ) -> None:
        super().__init__(name_val)
        self._database = database

    def object(self) -> List[MetadataValueInformationItem]:
        ret: List[MetadataValueInformationItem] = []
        for i in self._name_val:
            name = i[0]
            val = i[1]

            try:
                info = self._database.GetMetadataInformation(name)
            except Exception as ex:
                if is_error_with_text(ex, "Unknown metadata name: "):
                    raise ValueError("Unknown attribute: " + name) from ex
                raise ex

            try:
                value_info = info.GetValueInformation(val)
            except Exception as ex:
                if is_error_with_text(
                    ex, "The attribute '" + name + "' does not have a value called "
                ):
                    raise ValueError(
                        "Unknown attribute value: " + name + "," + val
                    ) from ex
                raise ex

            ret.append(
                MetadataValueInformationItem(
                    name, value_info.Value, value_info.Description, value_info.Comment
                )
            )
        return ret
