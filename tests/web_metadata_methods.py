# -*- coding: utf-8 -*-

from typing import List

from macrobond_financial.web.web_typs.metadata_value_information_response import \
    MetadataValueInformationResponse

from tests.test_common import TestCase


class WebMetadataMethods(TestCase):

    def test_web_get_value_information(self) -> None:
        actual = self.web_api.session.metadata.get_value_information(
            ('EntityType', 'Category'),
            ('EntityType', 'SuperRegion')
        )

        expected: List[MetadataValueInformationResponse] = [
            {
                'attributeName': 'EntityType',
                'value': 'Category',
                'description': 'Category'
            },
            {
                'attributeName': 'EntityType',
                'description': 'SuperRegion',
                'value': 'SuperRegion',
            }
        ]

        self.assertEqual(actual, expected)
