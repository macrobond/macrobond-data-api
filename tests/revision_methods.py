from typing import Any, cast
from datetime import datetime
import pytest

from pandas import DataFrame  # , Series as PdSeries,
from pandas.testing import assert_frame_equal
from macrobond_data_api.common.types import GetEntitiesError
from macrobond_data_api.common import Api
from macrobond_data_api.web import WebApi
from macrobond_data_api.com import ComApi


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_get_observation_history(api: Api) -> None:
    with pytest.raises(Exception, match="Not found bad name"):
        api.get_observation_history("bad name", datetime(2022, 3, 27))


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_get_vintage_series_error(api: Api) -> None:
    with pytest.raises(GetEntitiesError, match="failed to retrieve:\n\tnoseries! error_message: Not found"):
        api.get_vintage_series(datetime(2021, 4, 1), ["noseries!"])


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_get_vintage_series_revision_time_stamp_is_none(api: Api) -> None:
    data = api.get_vintage_series(datetime(1970, 4, 1), ["gbgdp"])
    assert data[0].revision_time_stamp is None


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_get_nth_release_values_is_float(api: Api) -> None:
    for i in range(2):
        obj = api.get_nth_release(i, ["gbgdp"])[0]
        assert isinstance(obj.values[0], float)


class TestCommon:
    def test_get_revision_info_to_pd_data_frame(self, web: WebApi, com: ComApi) -> None:
        assert 0 == len(
            DataFrame.compare(
                web.get_revision_info("usgdp")[0].to_pd_data_frame(),
                com.get_revision_info("usgdp")[0].to_pd_data_frame(),
            )
        ), "usgdp"

        assert 0 == len(
            DataFrame.compare(
                web.get_revision_info("ustrad4488")[0].to_pd_data_frame(),
                com.get_revision_info("ustrad4488")[0].to_pd_data_frame(),
            )
        ), "ustrad4488"

        assert 0 == len(
            DataFrame.compare(
                web.get_revision_info("ct_au_e_ao_c_22_v")[0].to_pd_data_frame(),
                com.get_revision_info("ct_au_e_ao_c_22_v")[0].to_pd_data_frame(),
            )
        ), "ct_au_e_ao_c_22_v"

    # get_vintage_series

    def test_get_vintage_series_values_to_pd_series(self, web: WebApi, com: ComApi) -> None:
        time_stamp = cast(datetime, web.get_revision_info("usgdp")[0].time_stamp_of_first_revision)
        assert_frame_equal(
            web.get_vintage_series(time_stamp, ["usgdp"])[0].values_to_pd_data_frame(),
            com.get_vintage_series(time_stamp, ["usgdp"])[0].values_to_pd_data_frame(),
        )

        time_stamp = cast(datetime, web.get_revision_info("ustrad4488")[0].time_stamp_of_first_revision)
        assert_frame_equal(
            web.get_vintage_series(time_stamp, ["ustrad4488"])[0].values_to_pd_data_frame(),
            com.get_vintage_series(time_stamp, ["ustrad4488"])[0].values_to_pd_data_frame(),
        )

    # get_nth_release

    def test_get_nth_release_values_to_pd_series(self, web: WebApi, com: ComApi) -> None:
        assert_frame_equal(
            web.get_nth_release(3, ["usgdp"])[0].values_to_pd_data_frame(),
            com.get_nth_release(3, ["usgdp"])[0].values_to_pd_data_frame(),
        )

        assert_frame_equal(
            web.get_nth_release(3, ["ustrad4488"])[0].values_to_pd_data_frame(),
            com.get_nth_release(3, ["ustrad4488"])[0].values_to_pd_data_frame(),
        )

        assert_frame_equal(
            web.get_nth_release(3, ["ct_au_e_ao_c_22_v"])[0].values_to_pd_data_frame(),
            com.get_nth_release(3, ["ct_au_e_ao_c_22_v"])[0].values_to_pd_data_frame(),
        )

    # get_all_vintage_series

    def test_get_all_vintage_series_1(self, web: WebApi, com: ComApi, test_metadata: Any, test_values: Any) -> None:
        web_r = web.get_all_vintage_series("usgdp")
        com_r = com.get_all_vintage_series("usgdp")

        test_metadata(web_r, com_r)

        for w_s, c_s in zip(web_r, com_r):
            test_values(w_s.values, c_s.values)
            w_s.values = c_s.values = []

        assert web_r == com_r

    def test_get_all_vintage_series_values_to_pd_series(self, web: WebApi, com: ComApi) -> None:
        # TODO: @mb-jp Needs rework

        # time is not included in com
        # self.assertEqual(
        #     0,
        #     len(
        #         PdSeries.compare(
        #             self.web_api.get_all_vintage_series("usgdp")[0].values_to_pd_series(),
        #             self.com_api.get_all_vintage_series("usgdp")[0].values_to_pd_series(),
        #         )
        #     ),
        #     "usgdp",
        # )

        # time is not included in com
        # self.assertEqual(
        #     0,
        #     len(
        #         PdSeries.compare(
        #             self.web_api.get_all_vintage_series("ustrad4488")[0].values_to_pd_series(),
        #             self.com_api.get_all_vintage_series("ustrad4488")[0].values_to_pd_series(),
        #         )
        #     ),
        #     "ustrad4488",
        # )

        assert_frame_equal(
            web.get_all_vintage_series("ct_au_e_ao_c_22_v")[0].values_to_pd_data_frame(),
            com.get_all_vintage_series("ct_au_e_ao_c_22_v")[0].values_to_pd_data_frame(),
        )

    # get_observation_history

    # def test_get_observation_history_to_pd_data_frame(self) -> None:

    # TODO: @mb-jp Needs rework

    # times = (
    #     datetime(2022, 3, 27),
    #     datetime(2021, 3, 27, 6, 17, 7),
    #     datetime(3000, 4, 1),
    # )
    # self.assertEqual(
    #     0,
    #     len(
    #         DataFrame.compare(
    #             self.web_api.get_observation_history("usgdp", *times)[0].to_pd_data_frame(),
    #             self.com_api.get_observation_history("usgdp", *times)[0].to_pd_data_frame(),
    #         )
    #     ),
    #     "usgdp",
    # )
    # self.assertEqual(
    #     0,
    #     len(
    #         DataFrame.compare(
    #             self.web_api.get_observation_history("ustrad4488", *times)[
    #                 0
    #             ].to_pd_data_frame(),
    #             self.com_api.get_observation_history("ustrad4488", *times)[
    #                 0
    #             ].to_pd_data_frame(),
    #         )
    #     ),
    #     "ustrad4488",
    # )
    # self.assertEqual(
    #     0,
    #     len(
    #         DataFrame.compare(
    #             self.web_api.get_observation_history("ct_au_e_ao_c_22_v", *times)[
    #                 0
    #             ].to_pd_data_frame(),
    #             self.com_api.get_observation_history("ct_au_e_ao_c_22_v", *times)[
    #                 0
    #             ].to_pd_data_frame(),
    #         )
    #     ),
    #     "ct_au_e_ao_c_22_v",
    # )

    # def test_get_observation_history_to_pd_series(self) -> None:

    # TODO: @mb-jp Needs rework

    # times = (
    #     datetime(2022, 3, 27),
    #     datetime(2021, 3, 27, 6, 17, 7),
    #     datetime(3000, 4, 1),
    # )

    # time is not included in com
    # self.assertEqual(
    #     0,
    #     len(
    #         PdSeries.compare(
    #             self.web_api.get_observation_history("usgdp", *times)[0].to_pd_series(),
    #             self.com_api.get_observation_history("usgdp", *times)[0].to_pd_series(),
    #         )
    #     ),
    #     "usgdp",
    # )

    # time is not included in com
    # self.assertEqual(
    #     0,
    #     len(
    #         PdSeries.compare(
    #             self.web_api.get_observation_history("ustrad4488", *times)[0].to_pd_series(),
    #             self.com_api.get_observation_history("ustrad4488", *times)[0].to_pd_series(),
    #         )
    #     ),
    #     "ustrad4488",
    # )

    # self.assertEqual(
    #     0,
    #     len(
    #         PdSeries.compare(
    #             self.web_api.get_observation_history("ct_au_e_ao_c_22_v", *times)[
    #                 0
    #             ].to_pd_series(),
    #             self.com_api.get_observation_history("ct_au_e_ao_c_22_v", *times)[
    #                 0
    #             ].to_pd_series(),
    #         )
    #     ),
    #     "ct_au_e_ao_c_22_v",
    # )

    def get_get_many_series_with_revisions__last_revision_adjustment_time_stamp(self) -> None:
        pytest.skip("not working now")

        # web = web_api()
        # com = com_api()

        # com_r = list(com.get_many_series_with_revisions([{"name": "usgdp"}]))[0]
        # web_r = list(web.get_many_series_with_revisions([{"name": "usgdp"}]))[0]

        # TODO: @mb-jp tidzone is not good : (

        # assert (
        #     com_r.metadata["LastRevisionAdjustmentTimeStamp"] == web_r.metadata["LastRevisionAdjustmentTimeStamp"]
        # ), "test metadata"
