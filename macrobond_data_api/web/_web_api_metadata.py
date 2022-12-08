# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING, List, Tuple

from macrobond_data_api.common.types import (
    MetadataValueInformation,
    MetadataValueInformationItem,
    MetadataAttributeInformation,
)

from .session import ProblemDetailsException

if TYPE_CHECKING:  # pragma: no cover
    from .web_api import WebApi


def metadata_list_values(self: "WebApi", name: str) -> MetadataValueInformation:
    values = self.session.metadata.list_attribute_values(name)
    return MetadataValueInformation(
        list(
            map(
                lambda x: MetadataValueInformationItem(
                    name, x["value"], x["description"], x.get("comment")
                ),
                values,
            )
        ),
        name,
    )


def metadata_get_attribute_information(
    self: "WebApi", *name: str
) -> List[MetadataAttributeInformation]:
    def get_metadata_attribute_information(info):
        return MetadataAttributeInformation(
            info["name"],
            info["description"],
            info.get("comment"),
            info["valueType"],
            info["usesValueList"],
            info["canListValues"],
            info["canHaveMultipleValues"],
            info["isDatabaseEntity"],
        )

    info = self.session.metadata.get_attribute_information(*name)
    return list(map(get_metadata_attribute_information, info))


def metadata_get_value_information(
    self: "WebApi", *name_val: Tuple[str, str]
) -> List[MetadataValueInformationItem]:
    ret: List[MetadataValueInformationItem] = []
    try:
        for info in self.session.metadata.get_value_information(*name_val):
            ret.append(
                MetadataValueInformationItem(
                    info["attributeName"],
                    info["value"],
                    info["description"],
                    info.get("comment"),
                )
            )
    except ProblemDetailsException as ex:
        if ex.status == 404:
            raise ValueError(ex.detail) from ex
        raise ex
    return ret
