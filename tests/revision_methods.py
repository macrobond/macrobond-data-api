from typing import Optional, cast, List
from datetime import datetime, timezone, timedelta
import pytest
from pandas import Series as PdSeries, DataFrame  # type: ignore
from macrobond_data_api.common.types import GetEntitiesError, RevisionHistoryRequest, SeriesWithVintagesErrorCode
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


class _Test_get_many_series_with_revisions:
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
    def test_out_liers(self, requests: List[RevisionHistoryRequest], web: WebApi, com: ComApi) -> None:
        for web_r, com_r in zip(
            list(web.get_many_series_with_revisions(requests)), list(com.get_many_series_with_revisions(requests))
        ):
            web_r.metadata = {}
            com_r.metadata = {}

            assert com_r.error_code == web_r.error_code

            assert len(com_r.vintages) == len(com_r.vintages)

            assert com_r == web_r

    def test_get_get_many_series_with_revisions_2(self, web: WebApi, com: ComApi) -> None:
        def test(
            request: RevisionHistoryRequest,
            error_code: Optional[SeriesWithVintagesErrorCode],
        ) -> None:
            for web_r, com_r in zip(
                list(web.get_many_series_with_revisions([request])),
                list(com.get_many_series_with_revisions([request])),
            ):
                web_r.metadata = {}
                com_r.metadata = {}

                assert com_r.error_code == web_r.error_code

                assert com_r.error_code == error_code

                assert len(com_r.vintages) == len(com_r.vintages)

                assert com_r == web_r

        vintage_series = com.get_all_vintage_series("usgdp")[:3]

        for vintage in vintage_series:
            metadata = vintage.metadata
            revision_time_stamp = vintage.revision_time_stamp
            last_modified_time = metadata["LastModifiedTimeStamp"]
            last_revision_adjustment = metadata["LastRevisionAdjustmentTimeStamp"]
            last_revision_time = metadata["LastRevisionTimeStamp"]

            # Test that we get the same result (no data) when we pass the current last modification timestamp
            request = RevisionHistoryRequest("usgdp", if_modified_since=last_modified_time)
            test(request, SeriesWithVintagesErrorCode.NOT_MODIFIED)

            # Test that we get the same result (some data) when we pass an older last modification timestamp
            request = RevisionHistoryRequest("usgdp", if_modified_since=last_modified_time - timedelta(seconds=1))
            test(request, None)

            # Since we do not pass last_revision_time, we will always get all revisions
            request = RevisionHistoryRequest(
                "usgdp",
                if_modified_since=last_modified_time - timedelta(seconds=1),
                last_revision_adjustment=last_revision_adjustment,
            )
            test(request, None)

            # Since neither last_revision_adjustment nor last_revision_time are changed,
            # we will always get all revisions. The metadata must have changed.
            request = RevisionHistoryRequest(
                "usgdp",
                if_modified_since=last_modified_time - timedelta(seconds=1),
                last_revision_adjustment=last_revision_adjustment,
                last_revision=last_revision_time,
            )
            test(request, None)

            # Since neither the last_revision_time is now and historical timestamp, we should get incremental updates
            request = RevisionHistoryRequest(
                "usgdp",
                if_modified_since=last_modified_time - timedelta(seconds=1),
                last_revision_adjustment=last_revision_adjustment,
                last_revision=revision_time_stamp,
            )
            test(request, None)

            # Since the last_revision_adjustment is now changed, we should get all the revisions
            request = RevisionHistoryRequest(
                "usgdp",
                if_modified_since=last_modified_time - timedelta(seconds=1),
                last_revision_adjustment=last_revision_adjustment - timedelta(seconds=1),
                last_revision=revision_time_stamp,
            )
            test(request, None)

    def _test(
        self,
        requests: List[RevisionHistoryRequest],
        web: WebApi,
        com: ComApi,
        error_code: Optional[SeriesWithVintagesErrorCode] = None,
    ) -> None:
        for web_r, com_r in zip(
            list(web.get_many_series_with_revisions(requests)), list(com.get_many_series_with_revisions(requests))
        ):
            web_r.metadata = {}
            com_r.metadata = {}

            if error_code:
                assert com_r.error_code == error_code

            assert com_r.error_code == web_r.error_code

            assert len(com_r.vintages) == len(com_r.vintages)

            assert com_r == web_r


class TestCommon:
    Test_get_many_series_with_revisions = _Test_get_many_series_with_revisions

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

    def test_get_all_vintage_series_1(self, web: WebApi, com: ComApi) -> None:
        web_r = web.get_all_vintage_series("usgdp")
        com_r = com.get_all_vintage_series("usgdp")

        for web_vintage, com_vintage in zip(web_r, com_r):
            keys = list(set(web_vintage.metadata.keys()) & set(com_vintage.metadata.keys()))
            keys.sort()

            assert len(keys) != 0

            for key in keys:
                if key == "DisplayUnit":
                    continue

                if isinstance(web_vintage.metadata[key], datetime):
                    web_datetime = web_vintage.metadata[key]
                    web_datetime = datetime(
                        web_datetime.year,
                        web_datetime.month,
                        web_datetime.day,
                        web_datetime.hour,
                        web_datetime.minute,
                        web_datetime.second,
                        # web_vintage.metadata[key].microsecond,
                        tzinfo=web_datetime.tzinfo,
                    )

                    com_datetime = com_vintage.metadata[key]
                    com_datetime = datetime(
                        com_datetime.year,
                        com_datetime.month,
                        com_datetime.day,
                        com_datetime.hour,
                        com_datetime.minute,
                        com_datetime.second,
                        # web_vintage.metadata[key].microsecond,
                        tzinfo=com_datetime.tzinfo,
                    )
                    assert web_datetime == com_datetime, "key " + key
                else:
                    if (
                        isinstance(web_vintage.metadata[key], list)
                        and not isinstance(com_vintage.metadata[key], list)
                        and len(web_vintage.metadata[key]) == 1
                    ):
                        assert web_vintage.metadata[key][0] == com_vintage.metadata[key], "key " + key
                    else:
                        assert web_vintage.metadata[key] == com_vintage.metadata[key], "key " + key

            web_vintage.metadata = {}
            com_vintage.metadata = {}

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
