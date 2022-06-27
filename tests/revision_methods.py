# -*- coding: utf-8 -*-

from datetime import datetime, timezone

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

    # onley on web for now
    def test_get_observation_history(self) -> None:
        api = self.web_api

        def get_datetime(
            year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0
        ) -> datetime:
            return datetime(year, month, day, hour, minute, second, microsecond).replace(
                tzinfo=timezone.utc
            )

        actual = api.get_observation_history(
            "usgdp",
            datetime(2022, 3, 27),
            datetime(2021, 3, 27, 6, 17, 7),
            datetime(3000, 4, 1),
        )

        expected = (
            SeriesObservationHistory(
                get_datetime(2022, 1, 1),
                (19735895000000, 19731119000000),
                (get_datetime(2022, 4, 28, 12, 31), get_datetime(2022, 5, 26, 12, 31)),
            ),
            SeriesObservationHistory(
                get_datetime(2021, 1, 1),
                (
                    19087568000000,
                    19088064000000,
                    19086375000000,
                    19055655000000,
                ),
                (
                    get_datetime(2021, 4, 29, 12, 33),
                    get_datetime(2021, 5, 27, 12, 31),
                    get_datetime(2021, 6, 24, 12, 31),
                    get_datetime(2021, 7, 29, 12, 31),
                ),
            ),
            SeriesObservationHistory(get_datetime(3000, 4, 1), (None,), (None,)),
        )

        self.assertSequenceEqual(actual, expected)

        self.assertEqual(float, type(actual[0].values[0]))

        # error

        with self.assertRaises(Exception) as context:
            api.get_observation_history("bad name", datetime(2022, 3, 27))

        self.assertEqual("Not found bad name", context.exception.args[0])


class Com(TestCase):
    def test_get_nth_release_values_is_float(self) -> None:
        get_nth_release_values_is_float(self, self.com_api)

    def test_get_vintage_series_error(self) -> None:
        get_vintage_series_error(self, self.com_api)

    def test_get_vintage_series_error_time(self) -> None:
        get_vintage_series_error_time(self, self.com_api)


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
