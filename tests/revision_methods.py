from typing import cast, List
from datetime import datetime, timezone
import pytest
from pandas import Series as PdSeries, DataFrame  # type: ignore
from macrobond_data_api.common.types import GetEntitiesError, RevisionHistoryRequest
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
        api.get_vintage_series(datetime(2021, 4, 1), "noseries!")


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_get_vintage_series_error_time(api: Api) -> None:
    with pytest.raises(ValueError, match="Invalid time"):
        api.get_vintage_series(datetime(1800, 4, 1), "gbgdp")


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_get_nth_release_values_is_float(api: Api) -> None:
    for i in range(2):
        obj = api.get_nth_release(i, "gbgdp")[0]
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
        assert 0 == len(
            PdSeries.compare(
                web.get_vintage_series(time_stamp, "usgdp")[0].values_to_pd_series(),
                com.get_vintage_series(time_stamp, "usgdp")[0].values_to_pd_series(),
            )
        ), "usgdp"

        time_stamp = cast(datetime, web.get_revision_info("ustrad4488")[0].time_stamp_of_first_revision)
        assert 0 == len(
            PdSeries.compare(
                web.get_vintage_series(time_stamp, "ustrad4488")[0].values_to_pd_series(),
                com.get_vintage_series(time_stamp, "ustrad4488")[0].values_to_pd_series(),
            )
        ), "ustrad4488"

    # get_nth_release

    def test_get_nth_release_values_to_pd_series(self, web: WebApi, com: ComApi) -> None:
        assert 0 == len(
            PdSeries.compare(
                web.get_nth_release(3, "usgdp")[0].values_to_pd_series(),
                com.get_nth_release(3, "usgdp")[0].values_to_pd_series(),
            )
        ), "usgdp"

        assert 0 == len(
            PdSeries.compare(
                web.get_nth_release(3, "ustrad4488")[0].values_to_pd_series(),
                com.get_nth_release(3, "ustrad4488")[0].values_to_pd_series(),
            )
        ), "ustrad4488"

        assert 0 == len(
            PdSeries.compare(
                web.get_nth_release(3, "ct_au_e_ao_c_22_v")[0].values_to_pd_series(),
                com.get_nth_release(3, "ct_au_e_ao_c_22_v")[0].values_to_pd_series(),
            )
        ), "ct_au_e_ao_c_22_v"

    # get_all_vintage_series

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

        assert 0 == len(
            PdSeries.compare(
                web.get_all_vintage_series("ct_au_e_ao_c_22_v")[0].values_to_pd_series(),
                com.get_all_vintage_series("ct_au_e_ao_c_22_v")[0].values_to_pd_series(),
            )
        ), "ct_au_e_ao_c_22_v"

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

    @pytest.mark.parametrize(
        "requests",
        [
            [],
            [RevisionHistoryRequest("usgdp")],
            [RevisionHistoryRequest("usgdp", if_modified_since=datetime(1, 1, 1, tzinfo=timezone.utc))],
            [RevisionHistoryRequest("usgdp", if_modified_since=datetime(9000, 1, 1, tzinfo=timezone.utc))],
            [RevisionHistoryRequest("usgdp", last_revision=datetime(1, 1, 1, tzinfo=timezone.utc))],
            [RevisionHistoryRequest("usgdp", last_revision=datetime(9000, 1, 1, tzinfo=timezone.utc))],
            [RevisionHistoryRequest("usgdp", last_revision_adjustment=datetime(1, 1, 1, tzinfo=timezone.utc))],
            [RevisionHistoryRequest("usgdp", last_revision_adjustment=datetime(9000, 1, 1, tzinfo=timezone.utc))],
        ],
        ids=[
            "[]",
            '[RevisionHistoryRequest("usgdp")]',
            "if modified since = datetime(1, 1, 1)",
            "if_modified_since = datetime(9000, 1, 1)",
            "last revision = datetime(1, 1, 1)",
            "last revision = datetime(9000, 1, 1)",
            "last revision adjustment = datetime(1, 1, 1)",
            "last revision adjustment = datetime(9000, 1, 1)",
        ],
    )
    def test_get_get_many_series_with_revisions(
        self, requests: List[RevisionHistoryRequest], web: WebApi, com: ComApi
    ) -> None:
        web_r = list(web.get_many_series_with_revisions(requests))
        com_r = list(com.get_many_series_with_revisions(requests))

        for results in zip(web_r, com_r):
            results[0].metadata = {}
            results[1].metadata = {}

        assert com_r == web_r


#    def test_get_get_many_series_with_revisions_2(self, com: ComApi) -> None:
#        vintage_series = com.get_all_vintage_series("usgdp")
#
#        for vintage in vintage_series:
#            metadata = vintage.metadata
#            revision_time_stamp = vintage.revision_time_stamp
#            last_modified_time = metadata["LastModifiedTimeStamp"]
#            last_revision_adjustment = metadata["LastRevisionAdjustmentTimeStamp"]
#            last_revision_time = metadata["LastRevisionTimeStamp"]
#
#            request = RevisionHistoryRequest("usgdp", if_modified_since=revision_time_stamp)
#
#            self.test_get_get_many_series_with_revisions([request])
#
#            request = RevisionHistoryRequest(
#                "usgdp", if_modified_since=revision_time_stamp, last_revision=revision_time_stamp
#            )
#
#            self.test_get_get_many_series_with_revisions([request])
