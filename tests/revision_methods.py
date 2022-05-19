# -*- coding: utf-8 -*-

from typing import Any, cast, TYPE_CHECKING

from datetime import datetime, timezone

from tests.test_common import TestCase

from macrobond_financial.common.typs import GetEntitiesError, SeriesObservationHistory

if TYPE_CHECKING:
    from macrobond_financial.common import Api


class Common(TestCase):

    # get_revision_info

    def test_get_revision_info_object(self) -> None:
        web = self.web_api.get_revision_info("usgdp").object()[0]
        com = self.com_api.get_revision_info("usgdp").object()[0]

        self.assertEqual(web.name, com.name)
        self.assertEqual(web.error_message, com.error_message)

        self.assertEqual(web.has_revisions, com.has_revisions)
        self.assertEqual(web.stores_revisions, com.stores_revisions)

        self.assertEqual(
            web.time_stamp_of_first_revision, com.time_stamp_of_first_revision
        )
        self.assertEqual(
            web.time_stamp_of_last_revision, com.time_stamp_of_last_revision
        )
        self.assertSequenceEqual(web.vintage_time_stamps, com.vintage_time_stamps)

    def test_get_revision_info_object_error(self) -> None:
        web = self.web_api.get_revision_info("noseries!", raise_error=False).object()[0]
        com = self.com_api.get_revision_info("noseries!", raise_error=False).object()[0]

        self.assertEqual(web.name, com.name)
        self.assertEqual(web.error_message, com.error_message)

        self.assertEqual(web.has_revisions, com.has_revisions)
        self.assertEqual(web.stores_revisions, com.stores_revisions)

        self.assertEqual(
            web.time_stamp_of_first_revision, com.time_stamp_of_first_revision
        )
        self.assertEqual(
            web.time_stamp_of_last_revision, com.time_stamp_of_last_revision
        )
        self.assertSequenceEqual(web.vintage_time_stamps, com.vintage_time_stamps)

    def test_get_revision_info_dict(self) -> None:
        web = self.web_api.get_revision_info("usgdp").dict()[0]
        com = self.com_api.get_revision_info("usgdp").dict()[0]

        self.assertDictEqual(web, com)

    def test_get_revision_info_dict_error(self) -> None:
        web = self.web_api.get_revision_info("noseries!", raise_error=False).dict()[0]
        com = self.com_api.get_revision_info("noseries!", raise_error=False).dict()[0]

        self.assertDictEqual(web, com)

    # get_vintage_series

    def test_get_vintage_series(self) -> None:
        info = self.web_api.get_revision_info("gbgdp").object()[0]

        time_stamp_of_last_revision = cast(datetime, info.time_stamp_of_last_revision)

        web = self.web_api.get_vintage_series(
            "gbgdp", time_stamp_of_last_revision
        ).object()
        com = self.com_api.get_vintage_series(
            "gbgdp", time_stamp_of_last_revision
        ).object()

        self.assertEqual(web.name, com.name, "name")
        self.assertEqual(web.primary_name, com.primary_name, "primary_name")
        self.assertEqual(web.title, com.title, "title")
        self.assertEqual(web.entity_type, com.entity_type, "entity_type")
        self.assertEqual(web.error_message, com.error_message, "error_message")
        self.assertEqual(web.is_error, com.is_error, "is_error")
        self.assertEqual(str(web), com.__str__(), "__str__() or str(series)")
        self.assertEqual(web.__repr__(), com.__repr__(), "__repr__")
        self.assertSequenceEqual(web.values, com.values, "values")
        self.assertSequenceEqual(web.dates, com.dates, "dates")
        self.assertEqual(
            web.revision_time_stamp, com.revision_time_stamp, "revision_time_stamp"
        )

        web = self.web_api.get_vintage_series(
            "noseries!", datetime(2021, 4, 1), raise_error=False
        ).object()
        com = self.com_api.get_vintage_series(
            "noseries!", datetime(2021, 4, 1), raise_error=False
        ).object()

        self.assertEqual(web.name, com.name, "name")
        self.assertEqual(web.error_message, com.error_message, "error_message")
        self.assertEqual(web.is_error, com.is_error, "is_error")
        self.assertEqual(str(web), com.__str__(), "__str__() or str(series)")
        self.assertEqual(web.__repr__(), com.__repr__(), "__repr__")
        self.assertSequenceEqual(web.values, com.values, "values")
        self.assertSequenceEqual(web.dates, com.dates, "dates")

    def test_get_vintage_series_dict(self) -> None:
        info = self.web_api.get_revision_info("gbgdp").object()[0]

        time_stamp_of_last_revision = cast(datetime, info.time_stamp_of_last_revision)

        web = self.web_api.get_vintage_series(
            "gbgdp", time_stamp_of_last_revision
        ).dict()
        com = self.com_api.get_vintage_series(
            "gbgdp", time_stamp_of_last_revision
        ).dict()

        def remove_metadata(obj: Any) -> Any:
            return dict(filter(lambda e: not e[0].startswith("metadata"), obj.items()))

        web = remove_metadata(web)
        com = remove_metadata(com)

        self.assertDictEqual(web, com)

        web = self.web_api.get_vintage_series(
            "noseries!", datetime(2021, 4, 1), False
        ).dict()
        com = self.com_api.get_vintage_series(
            "noseries!", datetime(2021, 4, 1), False
        ).dict()
        self.assertDictEqual(web, com)

    def test_get_vintage_series_data_frame(self) -> None:
        info = self.web_api.get_revision_info("gbgdp").object()[0]

        time_stamp_of_last_revision = cast(datetime, info.time_stamp_of_last_revision)

        web = self.web_api.get_vintage_series(
            "gbgdp", time_stamp_of_last_revision
        ).data_frame()
        com = self.com_api.get_vintage_series(
            "gbgdp", time_stamp_of_last_revision
        ).data_frame()

        self.assertEqual(len(web.columns), len(web.columns))

        def remove_metadata(data_frame):
            col = data_frame.columns
            ret = data_frame[
                [col for col in data_frame if not col.startswith("metadata.")]
            ]
            self.assertGreater(len(data_frame.columns), len(ret.columns))
            return ret

        web_no_metadata = remove_metadata(web)
        com_no_metadata = remove_metadata(com)

        self.assertDictEqual(web_no_metadata.to_dict(), com_no_metadata.to_dict())

    # get_nth_release

    def test_get_nth_release_object(self) -> None:
        for i in range(5):
            web = self.web_api.get_nth_release("gbgdp", i).object()
            com = self.com_api.get_nth_release("gbgdp", i).object()

            self.assertIsNotNone(web, "web is None")
            self.assertIsNotNone(com, "com is None")

            self.assertEqual(web.name, com.name, "name")
            self.assertEqual(web.primary_name, com.primary_name, "primary_name")
            self.assertEqual(web.title, com.title, "title")
            self.assertEqual(web.entity_type, com.entity_type, "entity_type")
            self.assertEqual(web.error_message, com.error_message, "error_message")
            self.assertEqual(web.is_error, com.is_error, "is_error")
            self.assertEqual(str(web), com.__str__(), "__str__() or str(series)")
            self.assertEqual(web.__repr__(), com.__repr__(), "__repr__")

            self.assertSequenceEqual(web.values, com.values, "values i = " + str(i))
            self.assertSequenceEqual(web.dates, com.dates, "dates i = " + str(i))

    def test_get_nth_release_data_frame(self) -> None:
        web = self.web_api.get_nth_release("gbgdp", 1).data_frame()
        com = self.com_api.get_nth_release("gbgdp", 1).data_frame()

        def remove_metadata_and_values(data_frame):
            col = data_frame.columns
            ret = data_frame[
                [
                    col
                    for col in data_frame
                    if not col.startswith("metadata.") and col != "Values"
                ]
            ]
            self.assertGreater(len(data_frame.columns), len(ret.columns))
            return ret

        web_no_metadata = remove_metadata_and_values(web)
        com_no_metadata = remove_metadata_and_values(com)

        self.assertDictEqual(web_no_metadata.to_dict(), com_no_metadata.to_dict())

    def test_get_nth_release_dict(self) -> None:
        web = self.web_api.get_nth_release("gbgdp", 1).dict()
        com = self.com_api.get_nth_release("gbgdp", 1).dict()

        def remove_metadata_and_values(target):
            return dict(
                (k, v)
                for k, v in target.items()
                if not k.startswith("metadata.") and k != "Values" and k != "Dates"
            )

        web = remove_metadata_and_values(web)
        com = remove_metadata_and_values(com)

        self.assertDictEqual(web, com)

    def test_get_nth_release_error(self) -> None:
        web = self.web_api.get_nth_release("bad name", 1, False).object()
        com = self.com_api.get_nth_release("bad name", 1, False).object()

        self.assertEqual(web, com)

    def test_get_nth_release_data_frame_error(self) -> None:
        web = self.web_api.get_nth_release("wiod_ltuc21_lvah49_p", 1).data_frame()
        com = self.com_api.get_nth_release("wiod_ltuc21_lvah49_p", 1).data_frame()

        def remove_metadata_and_values(data_frame):
            col = data_frame.columns
            ret = data_frame[
                [
                    col
                    for col in data_frame
                    if not col.startswith("metadata.")
                    and col != "Values"
                    and col != "Dates"
                ]
            ]
            self.assertGreater(len(data_frame.columns), len(ret.columns))
            return ret

        self.assertDictEqual(
            remove_metadata_and_values(web).to_dict(),
            remove_metadata_and_values(com).to_dict(),
        )

    def test_get_nth_release_dict_error(self) -> None:
        web = self.web_api.get_nth_release("wiod_ltuc21_lvah49_p", 1).dict()
        com = self.com_api.get_nth_release("wiod_ltuc21_lvah49_p", 1).dict()

        def remove_metadata_and_values(target):
            return dict(
                (k, v)
                for k, v in target.items()
                if not k.startswith("metadata.") and k != "Values" and k != "Dates"
            )

        web = remove_metadata_and_values(web)
        com = remove_metadata_and_values(com)

        self.assertDictEqual(web, com)


class Web(TestCase):
    def test_get_vintage_series_error(self) -> None:
        get_vintage_series_error(self, self.web_api)

    def test_get_vintage_series_error_time(self) -> None:
        get_vintage_series_error_time(self, self.web_api)

    # onley on web for now
    def test_get_observation_history(self) -> None:
        api = self.web_api

        def get_datetime(
            year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0
        ):
            return datetime(
                year, month, day, hour, minute, second, microsecond
            ).replace(tzinfo=timezone.utc)

        actual = api.get_observation_history(
            "usgdp",
            (
                datetime(2022, 3, 27),
                datetime(2021, 3, 27, 6, 17, 7),
                datetime(3000, 4, 1),
            ),
        ).object()

        expected = (
            SeriesObservationHistory(
                get_datetime(2022, 1, 1),
                (19735895000000,),
                (get_datetime(2022, 4, 28, 12, 31),),
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

        # error

        with self.assertRaises(Exception) as context:
            api.get_observation_history(
                "bad name",
                (datetime(2022, 3, 27),),
            ).object()

        self.assertEqual("Not found bad name", context.exception.args[0])


class Com(TestCase):
    def test_get_vintage_series_error(self) -> None:
        get_vintage_series_error(self, self.com_api)

    def test_get_vintage_series_error_time(self) -> None:
        get_vintage_series_error_time(self, self.com_api)


def get_vintage_series_error(test: TestCase, api: "Api") -> None:
    with test.assertRaises(GetEntitiesError) as context:
        api.get_vintage_series("noseries!", datetime(2021, 4, 1)).data_frame()

    test.assertEqual(
        "failed to retrieve:\n\tnoseries! error_message: Not found",
        context.exception.message,
    )


def get_vintage_series_error_time(test: TestCase, api: "Api") -> None:
    with test.assertRaises(ValueError) as context:
        api.get_vintage_series("gbgdp", datetime(1800, 4, 1)).data_frame()

    test.assertEqual("Invalid time", context.exception.args[0])
