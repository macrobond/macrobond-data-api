# -*- coding: utf-8 -*-

from macrobond_financial.common import Api
from macrobond_financial.common.meta_directory_methods import \
    MetadataAttributeInformation, MetadataValueInformation
from macrobond_financial.common.enums import MetadataAttributeType

from tests.test_common import TestCase


class Web(TestCase):
    def test_get_attribute_information(self) -> None:
        get_attribute_information(self, self.web_api)

    def test_list_values(self) -> None:
        list_values(self, self.web_api)


class Com(TestCase):
    def test_get_attribute_information(self) -> None:
        get_attribute_information(self, self.com_api)

    def test_list_values(self) -> None:
        list_values(self, self.com_api)


def get_attribute_information(test: TestCase, api: Api) -> None:
    actual = api.meta_directory.get_attribute_information("Description")
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

    with test.assertRaises(BaseException):
        api.meta_directory.get_attribute_information("Description____")


def list_values(test: TestCase, api: Api) -> None:
    values = api.meta_directory.list_values("RateType")

    actual = next(filter(lambda x: x.value == 'mole', values))
    expected = MetadataValueInformation(
        'RateType',
        'mole',
        'Mortgage Lending Rates',
        None
    )
    test.assertEqual(actual, expected)

    test.assertEqual(actual.__repr__(), "RateType", 'actual.__repr__()')

    with test.assertRaises(BaseException):
        api.meta_directory.list_values("__RateType")

    with test.assertRaises(BaseException):
        api.meta_directory.list_values("Description")
