# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from pandas import DataFrame  # type: ignore

from macrobond_financial.common import Api
from macrobond_financial.common.enums import MetadataAttributeType

from macrobond_financial.common.types import (
    MetadataValueInformationItem,
    MetadataAttributeInformation,
)

from tests.test_common import TestCase

if TYPE_CHECKING:
    from macrobond_financial.common.types import (
        TypedDictMetadataValueInformation,
        TypedDictMetadataAttributeInformation,
    )


class Web(TestCase):
    def test_get_attribute_information(self):
        get_attribute_information(self, self.web_api)

    def test_list_values(self):
        list_values(self, self.web_api)

    def test_get_value_information(self):
        get_value_information(self, self.web_api)


class Com(TestCase):
    def test_get_attribute_information(self):
        get_attribute_information(self, self.com_api)

    def test_list_values(self):
        list_values(self, self.com_api)

    def test_get_value_information(self):
        get_value_information(self, self.com_api)


def get_attribute_information(test: TestCase, api: Api) -> None:
    def _object() -> None:
        actual = api.metadata_get_attribute_information("Description")[0]
        expected = MetadataAttributeInformation(
            "Description",
            "Short description",
            "Contains part of an entity's title, along with other title generating attributes.",
            MetadataAttributeType.STRING,
            False,
            False,
            False,
            False,
        )
        test.assertEqual(actual, expected)

        test.assertEqual(actual.__repr__(), "Description", "actual.__repr__()")

    _object()

    def _dict() -> None:
        actual = api.metadata_get_attribute_information("Description")[0].to_dict()
        expected: "TypedDictMetadataAttributeInformation" = {
            "name": "Description",
            "description": "Short description",
            "comment": "Contains part of an entity's title,"
            + " along with other title generating attributes.",
            "value_type": MetadataAttributeType.STRING,
            "uses_value_list": False,
            "can_list_values": False,
            "can_have_multiple_values": False,
            "is_database_entity": False,
        }
        test.assertEqual(actual, expected)

    _dict()

    def _dataframe() -> None:
        value = api.metadata_get_attribute_information("Description")[0].data_frame()

        test.assertIsInstance(value, DataFrame)

        test.assertGreater(len(value), 0)

    _dataframe()

    with test.assertRaises(BaseException):
        api.metadata_get_attribute_information("Description____")


def list_values(test: TestCase, api: Api) -> None:
    def _object() -> None:
        value = api.metadata_list_values("RateType")

        actual = next(filter(lambda x: x.value == "mole", value))
        expected = MetadataValueInformationItem(
            "RateType", "mole", "Mortgage Lending Rates", None
        )

        test.assertEqual(actual, expected)

        test.assertEqual(actual.__repr__(), "mole")

    _object()

    def _dict() -> None:
        values = api.metadata_list_values("RateType").to_dict()

        actual = next(filter(lambda x: x["value"] == "mole", values))
        expected: "TypedDictMetadataValueInformation" = {
            "attribute_name": "RateType",
            "value": "mole",
            "description": "Mortgage Lending Rates",
            "comment": None,
        }
        test.assertEqual(actual, expected)

    _dict()

    def _dataframe() -> None:
        value = api.metadata_list_values("RateType").data_frame()

        test.assertIsInstance(value, DataFrame)

        test.assertGreater(len(value), 0)

    _dataframe()

    with test.assertRaises(BaseException):
        api.metadata_list_values("__RateType")

    with test.assertRaises(BaseException):
        api.metadata_list_values("Description")


def get_value_information(test: TestCase, api: Api) -> None:

    actual = api.metadata_get_value_information(("RateType", "mole"))
    expected = [
        MetadataValueInformationItem("RateType", "mole", "Mortgage Lending Rates", None)
    ]
    test.assertSequenceEqual(actual, expected)

    actual = api.metadata_get_value_information(
        ("RateType", "mole"), ("RateType", "fori")
    )
    expected = [
        MetadataValueInformationItem(
            "RateType", "mole", "Mortgage Lending Rates", None
        ),
        MetadataValueInformationItem(
            "RateType", "fori", "Foreign Institution Investments", None
        ),
    ]

    # erros

    with test.assertRaises(ValueError) as context:
        api.metadata_get_value_information(("bad val", "mole"))
    test.assertEqual(
        "Unknown attribute: bad val",
        str(context.exception),
    )

    with test.assertRaises(ValueError) as context:
        api.metadata_get_value_information(("RateType", "bad val"))
    test.assertEqual(
        "Unknown attribute value: RateType,bad val",
        str(context.exception),
    )

    with test.assertRaises(ValueError) as context:
        api.metadata_get_value_information(
            ("RateType", "mole"), ("RateType", "bad val")
        )
    test.assertEqual(
        "Unknown attribute value: RateType,bad val",
        str(context.exception),
    )
