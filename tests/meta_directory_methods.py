# -*- coding: utf-8 -*-

from macrobond_financial.common import Api
from macrobond_financial.common.meta_directory_methods import \
    MetadataAttributeInformation, MetadataValueInformation
from macrobond_financial.common.enums import MetadataAttributeType

from tests.test_common import TestCase


class MetaDirectoryMethods(TestCase):

    #  get_attribute_information

    def test_web_get_attribute_information(self) -> None:
        self.__get_attribute_information(self.web_api)

    def test_com_get_attribute_information(self) -> None:
        self.__get_attribute_information(self.com_api)

    def __get_attribute_information(self, api: Api) -> None:
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
        self.assertEqual(actual, expected)

        self.assertEqual(actual.__repr__(), "Description", 'actual.__repr__()')

        with self.assertRaises(BaseException):
            api.meta_directory.get_attribute_information("Description____")

    #  list_values

    def test_web_list_values(self) -> None:
        self.__list_values(self.web_api)

    def test_com_list_values(self) -> None:
        self.__list_values(self.com_api)

    def __list_values(self, api: Api) -> None:
        values = api.meta_directory.list_values("RateType")

        actual = next(filter(lambda x: x.value == 'mole', values))
        expected = MetadataValueInformation(
            'RateType',
            'mole',
            'Mortgage Lending Rates',
            None
        )
        self.assertEqual(actual, expected)

        self.assertEqual(actual.__repr__(), "RateType", 'actual.__repr__()')

        with self.assertRaises(BaseException):
            api.meta_directory.list_values("__RateType")

        with self.assertRaises(BaseException):
            api.meta_directory.list_values("Description")
