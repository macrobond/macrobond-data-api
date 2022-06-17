# -*- coding: utf-8 -*-

from typing import Any
from macrobond_financial.common import Api
from tests.test_common import TestCase


def run(test: TestCase, api: Api) -> None:

    # Metadata_list_values
    result: Any = api.metadata_list_values("RateType")
    result.to_pd_data_frame()
    result[0].to_pd_data_frame()
    result.to_dict()

    # Metadata_get_attribute_information
    result = api.metadata_get_attribute_information("Description")[0]
    result.to_pd_data_frame()
    result.to_dict()

    # Metadata_get_value_information
    result = api.metadata_get_value_information(("RateType", "mole"), ("RateType", "cobe"))[0]
    result.to_pd_data_frame()
    result.to_dict()


class Web(TestCase):
    def test(self) -> None:
        run(self, self.web_api)


class Com(TestCase):
    def test(self) -> None:
        run(self, self.com_api)
