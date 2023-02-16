from macrobond_data_api.web.web_types.metadata import MetadataValueInformationResponse
from macrobond_data_api.web import WebApi


def test_web_get_value_information(web: WebApi) -> None:
    actual = web.session.metadata.get_value_information(("EntityType", "Category"), ("EntityType", "SuperRegion"))

    expected: "MetadataValueInformationResponse" = [
        {
            "attributeName": "EntityType",
            "value": "Category",
            "description": "Category",
        },
        {
            "attributeName": "EntityType",
            "description": "SuperRegion",
            "value": "SuperRegion",
        },
    ]

    assert actual == expected
