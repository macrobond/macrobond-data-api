# -*- coding: utf-8 -*-

from typing import cast, TYPE_CHECKING

from datetime import datetime

from tests.test_common import TestCase

from macrobond_financial.common.typs import GetEntitiesError

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
        del web["MetaData"]
        del com["MetaData"]
        self.assertDictEqual(web, com)

        web = self.web_api.get_vintage_series(
            "noseries!", datetime(2021, 4, 1), raise_error=False
        ).dict()
        com = self.com_api.get_vintage_series(
            "noseries!", datetime(2021, 4, 1), raise_error=False
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
                [col for col in data_frame if not col.startswith("MetaData.")]
            ]
            self.assertGreater(len(data_frame.columns), len(ret.columns))
            return ret

        web_no_metadata = remove_metadata(web)
        com_no_metadata = remove_metadata(com)

        self.assertDictEqual(web_no_metadata.to_dict(), com_no_metadata.to_dict())


class Web(TestCase):
    def test_get_vintage_series_error(self) -> None:
        get_vintage_series_error(self, self.web_api)

    def test_get_vintage_series_error_time(self) -> None:
        get_vintage_series_error_time(self, self.web_api)


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
