# -*- coding: utf-8 -*-

from typing import Any

from macrobond_financial.common import Api
from tests.test_common import TestCase


def run(test: TestCase, api: Api) -> None:

    # Get_one_series
    result: Any = api.get_one_series("usgdp")
    result.to_pd_data_frame()
    result.to_dict()
    result.metadata_to_pd_series()
    result.values_to_pd_series()

    # Get_series
    result = api.get_series("usgdp")[0]
    result.to_pd_data_frame()
    result.to_dict()
    result.metadata_to_pd_series()

    # Get_one_entity
    result = api.get_one_entity("usgdp")
    result.to_pd_data_frame()
    result.to_dict()
    result.metadata_to_pd_series()

    # Get_entities
    result = api.get_entities("usgdp")[0]
    result.to_pd_data_frame()
    result.to_dict()
    result.metadata_to_pd_series()

    # Get_unified_series
    result = api.get_unified_series("usgdp", "uscpi")
    result.to_pd_data_frame()
    result.to_dict()


class Web(TestCase):
    def test(self) -> None:
        run(self, self.web_api)


class Com(TestCase):
    def test(self) -> None:
        run(self, self.com_api)
