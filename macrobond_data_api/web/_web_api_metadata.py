from typing import TYPE_CHECKING, Sequence, Tuple

from macrobond_data_api.common.types import (
    MetadataValueInformation,
    MetadataValueInformationItem,
    MetadataAttributeInformation,
)

from macrobond_data_api.common.types._repr_html_sequence import _ReprHtmlSequence

from .session import ProblemDetailsException

if TYPE_CHECKING:  # pragma: no cover
    from .web_api import WebApi


def metadata_list_values(self: "WebApi", name: str) -> MetadataValueInformation:
    return MetadataValueInformation(
        [
            MetadataValueInformationItem(name, x["value"], x["description"], x.get("comment"))
            for x in self.session.metadata.list_attribute_values(name)
        ],
        name,
    )


def metadata_get_attribute_information(self: "WebApi", *name: str) -> Sequence[MetadataAttributeInformation]:
    return _ReprHtmlSequence(
        [
            MetadataAttributeInformation(
                x["name"],
                x["description"],
                x.get("comment"),
                x["valueType"],
                x["usesValueList"],
                x["canListValues"],
                x["canHaveMultipleValues"],
                x["isDatabaseEntity"],
            )
            for x in self.session.metadata.get_attribute_information(*name)
        ]
    )


def metadata_get_value_information(
    self: "WebApi", *name_val: Tuple[str, str]
) -> Sequence[MetadataValueInformationItem]:
    try:
        return _ReprHtmlSequence(
            [
                MetadataValueInformationItem(x["attributeName"], x["value"], x["description"], x.get("comment"))
                for x in self.session.metadata.get_value_information(*name_val)
            ]
        )
    except ProblemDetailsException as ex:
        if ex.status == 404:
            raise ValueError(ex.detail) from ex
        raise ex
