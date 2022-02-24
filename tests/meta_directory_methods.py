# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from pandas import DataFrame  # type: ignore

from macrobond_financial.common import Api
from macrobond_financial.common.enums import MetadataAttributeType

from macrobond_financial.common.metadata_value_information import \
    MetadataValueInformation

from macrobond_financial.common.metadata_attribute_information import \
    MetadataAttributeInformation

from tests.test_common import TestCase

if TYPE_CHECKING:
    from macrobond_financial.common.metadata_value_information import \
        TypedDictMetadataValueInformation

    from macrobond_financial.common.metadata_attribute_information import \
        TypedDictMetadataAttributeInformation


class Web(TestCase):
    def test_get_attribute_information(self): get_attribute_information(self, self.web_api)
    def test_list_values(self): list_values(self, self.web_api)


class Com(TestCase):
    def test_get_attribute_information(self): get_attribute_information(self, self.com_api)
    def test_list_values(self): list_values(self, self.com_api)


def get_attribute_information(test: TestCase, api: Api) -> None:
    def _object() -> None:
        actual = api.meta_directory.get_attribute_information("Description").object()
        expected = MetadataAttributeInformation(
            'Description',
            'Short description',
            "Contains part of an entity's title, along with other title generating attributes.",
            MetadataAttributeType.STRING,
            False,
            False,
            False,
            False
        )
        test.assertEqual(actual, expected)

        test.assertEqual(actual.__repr__(), "Description", 'actual.__repr__()')
    _object()

    def _dict() -> None:
        actual = api.meta_directory.get_attribute_information("Description").dict()
        expected: 'TypedDictMetadataAttributeInformation' = {
            'name': 'Description',
            'description': 'Short description',
            'comment':
                "Contains part of an entity's title, along with other title generating attributes.",
            'value_type': MetadataAttributeType.STRING,
            'uses_value_list': False,
            'can_list_values': False,
            'can_have_multiple_values': False,
            'is_database_entity': False
        }
        test.assertEqual(actual, expected)
    _dict()

    def _dataframe() -> None:
        value = api.meta_directory.get_attribute_information("Description").data_frame()

        test.assertIsInstance(value, DataFrame)

        test.assertGreater(len(value), 0)
    _dataframe()

    with test.assertRaises(BaseException):
        api.meta_directory.get_attribute_information("Description____").object()


def list_values(test: TestCase, api: Api) -> None:
    def _object() -> None:
        values = api.meta_directory.list_values("RateType").list_of_objects()

        actual = next(filter(lambda x: x.value == 'mole', values))
        expected = MetadataValueInformation(
            'RateType',
            'mole',
            'Mortgage Lending Rates',
            None
        )
        test.assertEqual(actual, expected)

        test.assertEqual(actual.__repr__(), "RateType", 'actual.__repr__()')

    _object()

    def _dict() -> None:
        values = api.meta_directory.list_values("RateType").list_of_dicts()

        actual = next(filter(lambda x: x['value'] == 'mole', values))
        expected: 'TypedDictMetadataValueInformation' = {
            'attribute_name': 'RateType',
            'value': 'mole',
            'description': 'Mortgage Lending Rates',
            'comment': None
        }
        test.assertEqual(actual, expected)
    _dict()

    def _dataframe() -> None:
        value = api.meta_directory.list_values("RateType").data_frame()

        test.assertIsInstance(value, DataFrame)

        test.assertGreater(len(value), 0)
    _dataframe()

    with test.assertRaises(BaseException):
        api.meta_directory.list_values("__RateType").list_of_objects()

    with test.assertRaises(BaseException):
        api.meta_directory.list_values("Description").list_of_objects()
