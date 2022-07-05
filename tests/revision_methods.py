# -*- coding: utf-8 -*-

from typing import cast

from datetime import datetime, timezone

from pandas import Series as PdSeries, DataFrame  # type: ignore

from tests.test_common import TestCase

from macrobond_financial.common.types import GetEntitiesError, SeriesObservationHistory

from macrobond_financial.common import Api


class Web(TestCase):
    def test_get_nth_release_values_is_float(self) -> None:
        get_nth_release_values_is_float(self, self.web_api)

    def test_get_vintage_series_error(self) -> None:
        get_vintage_series_error(self, self.web_api)

    def test_get_vintage_series_error_time(self) -> None:
        get_vintage_series_error_time(self, self.web_api)

    def test_get_observation_history(self) -> None:
        get_observation_history(self, self.web_api)


class Com(TestCase):
    def test_get_nth_release_values_is_float(self) -> None:
        get_nth_release_values_is_float(self, self.com_api)

    def test_get_vintage_series_error(self) -> None:
        get_vintage_series_error(self, self.com_api)

    def test_get_vintage_series_error_time(self) -> None:
        get_vintage_series_error_time(self, self.com_api)

    def test_get_observation_history(self) -> None:
        get_observation_history(self, self.com_api)


def get_observation_history(test: TestCase, api: Api) -> None:
    with test.assertRaises(Exception) as context:
        api.get_observation_history("bad name", datetime(2022, 3, 27))

    test.assertEqual("Not found bad name", context.exception.args[0])


def get_vintage_series_error(test: TestCase, api: Api) -> None:
    with test.assertRaises(GetEntitiesError) as context:
        api.get_vintage_series(datetime(2021, 4, 1), "noseries!")

    test.assertEqual(
        "failed to retrieve:\n\tnoseries! error_message: Not found",
        context.exception.message,
    )


def get_vintage_series_error_time(test: TestCase, api: Api) -> None:
    with test.assertRaises(ValueError) as context:
        api.get_vintage_series(datetime(1800, 4, 1), "gbgdp")

    test.assertEqual("Invalid time", context.exception.args[0])


def get_nth_release_values_is_float(test: TestCase, api: Api) -> None:
    for i in range(2):
        obj = api.get_nth_release(i, "gbgdp")[0]
        test.assertEqual(float, type(obj.values[0]))


class Common(TestCase):

    # get_revision_info

    def test_get_revision_info_to_pd_data_frame(self) -> None:
        self.assertEqual(
            0,
            len(
                DataFrame.compare(
                    self.web_api.get_revision_info("usgdp")[0].to_pd_data_frame(),
                    self.com_api.get_revision_info("usgdp")[0].to_pd_data_frame(),
                )
            ),
            "usgdp",
        )
        self.assertEqual(
            0,
            len(
                DataFrame.compare(
                    self.web_api.get_revision_info("ustrad4488")[0].to_pd_data_frame(),
                    self.com_api.get_revision_info("ustrad4488")[0].to_pd_data_frame(),
                )
            ),
            "ustrad4488",
        )
        self.assertEqual(
            0,
            len(
                DataFrame.compare(
                    self.web_api.get_revision_info("ct_au_e_ao_c_22_v")[0].to_pd_data_frame(),
                    self.com_api.get_revision_info("ct_au_e_ao_c_22_v")[0].to_pd_data_frame(),
                )
            ),
            "ct_au_e_ao_c_22_v",
        )

    # get_vintage_series

    def test_get_vintage_series_values_to_pd_series(self) -> None:
        time_stamp = cast(
            datetime, self.web_api.get_revision_info("usgdp")[0].time_stamp_of_first_revision
        )
        self.assertEqual(
            0,
            len(
                PdSeries.compare(
                    self.web_api.get_vintage_series(time_stamp, "usgdp")[0].values_to_pd_series(),
                    self.com_api.get_vintage_series(time_stamp, "usgdp")[0].values_to_pd_series(),
                )
            ),
            "usgdp",
        )
        time_stamp = cast(
            datetime, self.web_api.get_revision_info("ustrad4488")[0].time_stamp_of_first_revision
        )
        self.assertEqual(
            0,
            len(
                PdSeries.compare(
                    self.web_api.get_vintage_series(time_stamp, "ustrad4488")[
                        0
                    ].values_to_pd_series(),
                    self.com_api.get_vintage_series(time_stamp, "ustrad4488")[
                        0
                    ].values_to_pd_series(),
                )
            ),
            "ustrad4488",
        )

    # get_nth_release

    def test_get_nth_release_values_to_pd_series(self) -> None:
        self.assertEqual(
            0,
            len(
                PdSeries.compare(
                    self.web_api.get_nth_release(3, "usgdp")[0].values_to_pd_series(),
                    self.com_api.get_nth_release(3, "usgdp")[0].values_to_pd_series(),
                )
            ),
            "usgdp",
        )
        self.assertEqual(
            0,
            len(
                PdSeries.compare(
                    self.web_api.get_nth_release(3, "ustrad4488")[0].values_to_pd_series(),
                    self.com_api.get_nth_release(3, "ustrad4488")[0].values_to_pd_series(),
                )
            ),
            "ustrad4488",
        )
        self.assertEqual(
            0,
            len(
                PdSeries.compare(
                    self.web_api.get_nth_release(3, "ct_au_e_ao_c_22_v")[0].values_to_pd_series(),
                    self.com_api.get_nth_release(3, "ct_au_e_ao_c_22_v")[0].values_to_pd_series(),
                )
            ),
            "ct_au_e_ao_c_22_v",
        )

    # get_all_vintage_series

    def test_get_all_vintage_series_values_to_pd_series(self) -> None:

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

        self.assertEqual(
            0,
            len(
                PdSeries.compare(
                    self.web_api.get_all_vintage_series("ct_au_e_ao_c_22_v")[
                        0
                    ].values_to_pd_series(),
                    self.com_api.get_all_vintage_series("ct_au_e_ao_c_22_v")[
                        0
                    ].values_to_pd_series(),
                )
            ),
            "ct_au_e_ao_c_22_v",
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
