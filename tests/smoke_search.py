# -*- coding: utf-8 -*-

from typing import Any

from macrobond_financial.common.types import SearchFilter
from macrobond_financial.common import Api
from tests.test_common import TestCase


def run(test: TestCase, api: Api) -> None:

    # Entity_search
    result: Any = api.entity_search("usgdp")
    result.to_pd_data_frame()
    result.to_dict()

    # Entity_search_multi_filter
    result = api.entity_search_multi_filter(SearchFilter("usgdp"))
    result.to_pd_data_frame()
    result.to_dict()


class Web(TestCase):
    def test(self) -> None:
        run(self, self.web_api)


class Com(TestCase):
    def test(self) -> None:
        run(self, self.com_api)
