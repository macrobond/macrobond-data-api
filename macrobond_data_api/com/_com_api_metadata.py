# -*- coding: utf-8 -*-

from typing import List, Tuple, TYPE_CHECKING, cast

from macrobond_data_api.common.types import (
    MetadataValueInformationItem,
    MetadataAttributeInformation,
    MetadataValueInformation,
)

if TYPE_CHECKING:  # pragma: no cover
    from .com_api import ComApi

    from macrobond_data_api.common.enums import MetadataAttributeType


def metadata_list_values(self: "ComApi", name: str) -> MetadataValueInformation:
    info = self.database.GetMetadataInformation(name)
    values = info.ListAllValues()

    return MetadataValueInformation(
        list(
            map(
                lambda x: MetadataValueInformationItem(name, x.Value, x.Description, x.Comment),
                values,
            )
        ),
        name,
    )


def metadata_get_attribute_information(
    self: "ComApi", *names: str
) -> List[MetadataAttributeInformation]:
    def get_metadata_attribute_information(name: str):
        info = self.database.GetMetadataInformation(name)
        return MetadataAttributeInformation(
            info.Name,
            info.Description,
            info.Comment,
            cast("MetadataAttributeType", info.ValueType),
            info.UsesValueList,
            info.CanListValues,
            info.CanHaveMultipleValues,
            info.IsDatabaseEntity,
        )

    return list(map(get_metadata_attribute_information, names))


def metadata_get_value_information(
    self: "ComApi", *name_val: Tuple[str, str]
) -> List[MetadataValueInformationItem]:
    def is_error_with_text(ex: Exception, text: str) -> bool:
        return len(ex.args) >= 3 and len(ex.args[2]) >= 3 and ex.args[2][2].startswith(text)

    ret: List[MetadataValueInformationItem] = []
    for i in name_val:
        name = i[0]
        val = i[1]

        try:
            info = self.database.GetMetadataInformation(name)
        except Exception as ex:
            if is_error_with_text(ex, "Unknown metadata name: "):
                raise ValueError("Unknown attribute: " + name) from ex
            raise ex

        try:
            value_info = info.GetValueInformation(val)
        except Exception as ex:
            if is_error_with_text(ex, "The attribute '" + name + "' does not have a value called "):
                raise ValueError("Unknown attribute value: " + name + "," + val) from ex
            raise ex

        ret.append(
            MetadataValueInformationItem(
                name, value_info.Value, value_info.Description, value_info.Comment
            )
        )
    return ret
