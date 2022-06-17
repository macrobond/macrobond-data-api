# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any

from macrobond_financial.common import Api
from tests.test_common import TestCase


def run(test: TestCase, api: Api) -> None:

    # get_revision_info
    result: Any = api.get_revision_info("usgdp")[0]
    result.to_pd_data_frame()
    result.to_dict()

    # Get_vintage_series
    last_revision = api.get_revision_info("gbgdp")[0].time_stamp_of_last_revision

    if not last_revision:
        raise ValueError("last_revision is None")

    result = api.get_vintage_series(last_revision, "gbgdp")[0]
    result.to_pd_data_frame()
    result.metadata_to_pd_series()
    result.to_dict()

    # Get_nth_release
    result = api.get_nth_release(4, "gbgdp")[0]
    result.to_pd_data_frame()
    result.to_dict()

    # Get_all_vintage_series
    result = api.get_all_vintage_series("usgdp")[0]
    result.to_pd_data_frame()
    result.to_dict()


class Web(TestCase):
    def test(self) -> None:
        run(self, self.web_api)

        api = self.web_api

        # Get_observation_history
        result = api.get_observation_history("usgdp", datetime(2022, 3, 27))[0]
        result.to_pd_data_frame()
        result.to_dict()
        result.to_pd_series()


class Com(TestCase):
    def test(self) -> None:
        run(self, self.com_api)
