from datetime import datetime
from pandas import Series as PdSeries  # type: ignore

from macrobond_data_api.common import Api
from tests.test_common import TestCase


def run(test: TestCase, api: Api) -> None:  # pylint: disable=unused-argument
    # get_revision_info
    result1 = api.get_revision_info("usgdp")[0]
    str(result1.to_pd_data_frame())
    result1.to_dict()

    # Get_vintage_series
    last_revision = api.get_revision_info("gbgdp")[0].time_stamp_of_last_revision

    if not last_revision:
        raise ValueError("last_revision is None")

    result2 = api.get_vintage_series(last_revision, "gbgdp")[0]
    str(result2.values_to_pd_series())
    str(result2.metadata_to_pd_series())
    result2.to_dict()

    # Get_nth_release
    result3 = api.get_nth_release(4, "gbgdp")[0]
    str(result3.values_to_pd_series())
    str(result3.metadata_to_pd_series())
    result3.to_dict()

    #    # Get_all_vintage_series
    result4 = api.get_all_vintage_series("usgdp")[0]
    str(result4.values_to_pd_series())
    str(result4.metadata_to_pd_series())
    result4.to_dict()

    # Get_observation_history
    result5 = api.get_observation_history("usgdp", datetime(2022, 3, 27))[0]
    str(result5.to_pd_data_frame())
    result5.to_dict()
    result5.to_pd_series()


class Web(TestCase):
    def test(self) -> None:
        self.assertNoWarnings(lambda: run(self, self.web_api))


class Com(TestCase):
    def test(self) -> None:
        self.assertNoWarnings(lambda: run(self, self.com_api))


class Common(TestCase):
    def test(self) -> None:
        PdSeries.compare(
            self.web_api.get_all_vintage_series("usgdp")[0].values_to_pd_series(),
            self.com_api.get_all_vintage_series("usgdp")[0].values_to_pd_series(),
        )

        PdSeries.compare(
            self.web_api.get_all_vintage_series("ustrad4488")[0].values_to_pd_series(),
            self.com_api.get_all_vintage_series("ustrad4488")[0].values_to_pd_series(),
        )

        PdSeries.compare(
            self.web_api.get_all_vintage_series("ct_au_e_ao_c_22_v")[0].values_to_pd_series(),
            self.com_api.get_all_vintage_series("ct_au_e_ao_c_22_v")[0].values_to_pd_series(),
        )
