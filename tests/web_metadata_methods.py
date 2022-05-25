# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from tests.test_common import TestCase

if TYPE_CHECKING:  # pragma: no cover
    from macrobond_financial.web.web_types import MetadataValueInformationResponse


class WebMetadataMethods(TestCase):
    def test_web_get_value_information(self) -> None:
        actual = self.web_api.session.metadata.get_value_information(
            ("EntityType", "Category"), ("EntityType", "SuperRegion")
        )

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

        self.assertEqual(actual, expected)
