from typing import Sequence, Tuple, TYPE_CHECKING, cast

from macrobond_data_api.common.types import (
    MetadataValueInformationItem,
    MetadataAttributeInformation,
    MetadataValueInformation,
)

from macrobond_data_api.common.types._repr_html_sequence import _ReprHtmlSequence

if TYPE_CHECKING:  # pragma: no cover
    from .com_api import ComApi

    from macrobond_data_api.common.enums import MetadataAttributeType


def metadata_list_values(self: "ComApi", name: str) -> MetadataValueInformation:
    info = self.database.GetMetadataInformation(name)
    values = info.ListAllValues()

    return MetadataValueInformation(
        [MetadataValueInformationItem(name, x.Value, x.Description, x.Comment) for x in values],
        name,
    )


def metadata_get_attribute_information(self: "ComApi", *names: str) -> Sequence[MetadataAttributeInformation]:
    return _ReprHtmlSequence(
        [
            MetadataAttributeInformation(
                x.Name,
                x.Description,
                x.Comment,
                cast("MetadataAttributeType", x.ValueType),
                x.UsesValueList,
                x.CanListValues,
                x.CanHaveMultipleValues,
                x.IsDatabaseEntity,
            )
            for x in (self.database.GetMetadataInformation(x) for x in names)
        ]
    )


def metadata_get_value_information(
    self: "ComApi", *name_val: Tuple[str, str]
) -> Sequence[MetadataValueInformationItem]:
    def is_error_with_text(ex: Exception, text: str) -> bool:
        return len(ex.args) >= 3 and len(ex.args[2]) >= 3 and ex.args[2][2].startswith(text)

    def to_obj(name: str, val: str) -> MetadataValueInformationItem:
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

        return MetadataValueInformationItem(name, value_info.Value, value_info.Description, value_info.Comment)

    return _ReprHtmlSequence([to_obj(x[0], x[1]) for x in name_val])
