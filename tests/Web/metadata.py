# -*- coding: utf-8 -*-


from unittest import TestCase  # type: ignore

from macrobond_financial.web import WebClient
from macrobond_financial.com import ComClient

from macrobond_financial.common.types import SearchFilter


class Metadata(TestCase):
    def test_get_200(self) -> None:
        with ComClient() as com_api:
            with WebClient() as web_api:
                com_metadata = com_api.get_one_entity("usgdp").metadata
                web_metadata = web_api.get_one_entity("usgdp").metadata
                print(web_metadata)
                ...

    def test_1(self) -> None:
        with ComClient() as com_api:
            with WebClient() as web_api:
                r = web_api.entity_search_multi_filter_long(SearchFilter("usgdp"))
                ...
                print(r)
                ...
