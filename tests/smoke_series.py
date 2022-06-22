# -*- coding: utf-8 -*-

from macrobond_financial.common import Api
from tests.test_common import TestCase


def run(test: TestCase, api: Api) -> None:  # pylint: disable=unused-argument

    # Get_one_series
    result1 = api.get_one_series("usgdp")
    str(result1.values_to_pd_series())
    str(result1.metadata_to_pd_series())
    result1.to_dict()

    # Get_series
    result2 = api.get_series("usgdp")[0]
    str(result2.values_to_pd_series())
    str(result2.metadata_to_pd_series())
    result2.to_dict()

    # Get_one_entity
    result3 = api.get_one_entity("usgdp")
    str(result3.metadata_to_pd_series())
    result3.to_dict()

    # Get_entities
    result4 = api.get_entities("usgdp")[0]
    str(result4.metadata_to_pd_series())
    result4.to_dict()

    # Get_unified_series
    result5 = api.get_unified_series("usgdp", "uscpi")
    str(result5.to_pd_data_frame())
    result5.to_dict()


class Web(TestCase):
    def test(self) -> None:
        self.assertNoWarnings(lambda: run(self, self.web_api))


class Com(TestCase):
    def test(self) -> None:
        self.assertNoWarnings(lambda: run(self, self.com_api))
