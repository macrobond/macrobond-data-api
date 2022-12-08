# -*- coding: utf-8 -*-

from macrobond_data_api.common import Api
from tests.test_common import TestCase


def run(test: TestCase, api: Api) -> None:  # pylint: disable=unused-argument

    # Metadata_list_values
    result1 = api.metadata_list_values("RateType")
    str(result1.to_pd_data_frame())
    str(result1[0].to_pd_data_frame())
    result1.to_dict()

    # Metadata_get_attribute_information
    result2 = api.metadata_get_attribute_information("Description")[0]
    str(result2.to_pd_data_frame())
    result2.to_dict()

    # Metadata_get_value_information
    result3 = api.metadata_get_value_information(("RateType", "mole"), ("RateType", "cobe"))[0]
    str(result3.to_pd_data_frame())
    result3.to_dict()


class Web(TestCase):
    def test(self) -> None:
        self.assertNoWarnings(lambda: run(self, self.web_api))


class Com(TestCase):
    def test(self) -> None:
        self.assertNoWarnings(lambda: run(self, self.com_api))
