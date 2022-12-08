# -*- coding: utf-8 -*-

from typing import List
from unittest import skip  # type: ignore[attr-defined]
from macrobond_data_api.web import (
    SubscriptionBody,
    SubscriptionListItem,
    create_revision_history_request,
)
from macrobond_data_api.common import Api
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

    @skip("needs access")
    def test_get_subscription_list(self) -> None:
        def _run():
            result = self.web_api.get_subscription_list()  # pylint: disable=unused-variable
            breakpoint()  # pylint: disable=forgotten-debug-statement

        self.assertNoWarnings(_run)

    @skip("needs access")
    def test_get_subscription_list_iterative(self) -> None:
        def empty_method_1(body: SubscriptionBody) -> bool:  # pylint: disable=unused-argument
            return True

        def empty_method_2(
            items: List[SubscriptionListItem],  # pylint: disable=unused-argument
        ) -> bool:
            return True

        self.assertNoWarnings(
            lambda: self.web_api.get_subscription_list_iterative(empty_method_1, empty_method_2)
        )

    @skip("needs access")
    def test_get_fetch_all_vintageseries(self) -> None:
        def _run():
            def empty_method_1(arg):  # pylint: disable=unused-argument
                ...

            self.web_api.get_fetch_all_vintageseries(
                empty_method_1,
                [
                    create_revision_history_request("usgdp"),
                    create_revision_history_request("uscpi"),
                ],
            )

        self.assertNoWarnings(_run)


class Com(TestCase):
    def test(self) -> None:
        self.assertNoWarnings(lambda: run(self, self.com_api))
