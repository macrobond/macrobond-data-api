# -*- coding: utf-8 -*-

from macrobond_data_api.common import Api
from tests.test_common import TestCase


class Web(TestCase):
    def test_get_attribute_information(self) -> None:
        get_attribute_information(self, self.web_api)

    def test_list_values(self) -> None:
        list_values(self, self.web_api)

    def test_get_value_information(self) -> None:
        get_value_information(self, self.web_api)


class Com(TestCase):
    def test_get_attribute_information(self) -> None:
        get_attribute_information(self, self.com_api)

    def test_list_values(self) -> None:
        list_values(self, self.com_api)

    def test_get_value_information(self) -> None:
        get_value_information(self, self.com_api)


def get_attribute_information(test: TestCase, api: Api) -> None:
    with test.assertRaises(BaseException):
        api.metadata_get_attribute_information("Description____")


def list_values(test: TestCase, api: Api) -> None:

    with test.assertRaises(BaseException):
        api.metadata_list_values("__RateType")

    with test.assertRaises(BaseException):
        api.metadata_list_values("Description")


def get_value_information(test: TestCase, api: Api) -> None:

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
        api.metadata_get_value_information(("RateType", "mole"), ("RateType", "bad val"))
    test.assertEqual(
        "Unknown attribute value: RateType,bad val",
        str(context.exception),
    )
