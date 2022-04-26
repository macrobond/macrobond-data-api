# -*- coding: utf-8 -*-

from datetime import datetime

from typing import TYPE_CHECKING

from macrobond_financial.common import Api
from macrobond_financial.common.typs import (
    SeriesEntry,
    StartOrEndPoint,
    GetEntitiesError,
)
from macrobond_financial.common.enums import SeriesMissingValueMethod, SeriesFrequency

from tests.test_common import TestCase

if TYPE_CHECKING:
    from macrobond_financial.common.typs import UnifiedSeriesDict


def comper_unified_dict(
    test: TestCase, a_unified: "UnifiedSeriesDict", b_unified: "UnifiedSeriesDict"
) -> None:
    test.assertNotEqual(len(a_unified["dates"]), 0)

    test.assertSequenceEqual(a_unified["dates"], b_unified["dates"])

    test.assertEqual(len(a_unified["series"]), len(b_unified["series"]))
    for i, a_series in enumerate(a_unified["series"]):
        b_series = b_unified["series"][i]
        test.assertEqual(a_series["name"], b_series["name"])
        test.assertEqual(a_series["error_message"], b_series["error_message"])

        if a_series["error_message"] != "":
            test.assertSequenceEqual(a_series["values"], b_series["values"])
            test.assertDictEqual(a_series["metadata"], b_series["metadata"])


class Common(TestCase):
    def test_get_one_series(self) -> None:
        web = self.web_api.get_one_series("usgdp").object()
        com = self.com_api.get_one_series("usgdp").object()

        # intersection = [
        #     value for value in web.metadata.keys()
        #     if value in com.metadata.keys()
        # ]

        # for key in intersection:
        #     self.assertEqual(
        #         web.metadata[key], com.metadata[key], 'metadata key = ' + key
        #     )

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

    def test_get_one_entity(self) -> None:
        web = self.web_api.get_one_entity("usgdp").object()
        com = self.com_api.get_one_entity("usgdp").object()

        self.assertEqual(web.name, com.name, "name")
        self.assertEqual(web.primary_name, com.primary_name, "primary_name")
        self.assertEqual(web.title, com.title, "title")
        self.assertEqual(web.entity_type, com.entity_type, "entity_type")
        self.assertEqual(web.error_message, com.error_message, "error_message")
        self.assertEqual(web.is_error, com.is_error, "is_error")
        self.assertEqual(str(web), com.__str__(), "__str__() or str(series)")
        self.assertEqual(web.__repr__(), com.__repr__(), "__repr__")

    def test_get_one_entity_metadata_as_data_frame(self) -> None:
        web = self.web_api.get_one_entity("usgdp").metadata_as_data_frame()
        com = self.com_api.get_one_entity("usgdp").metadata_as_data_frame()

        self.assertSequenceEqual(web.columns, com.columns)

        web_dict = web.to_dict()["Attributes"]
        com_dict = com.to_dict()["Attributes"]

        self.assertIsNotNone(web_dict.get("Category"))
        self.assertEqual(web_dict.get("Category"), com_dict.get("Category"))

        self.assertIsNotNone(web_dict.get("Currency"))
        self.assertEqual(web_dict.get("Currency"), com_dict.get("Currency"))

    def test_get_unified_series_dict(self) -> None:
        web = self.web_api.get_unified_series(
            "usgdp",
            "uscpi",
        ).dict()

        com = self.com_api.get_unified_series(
            "usgdp",
            "uscpi",
        ).dict()

        comper_unified_dict(self, web, com)

        web = self.web_api.get_unified_series(
            "usgdp", "uscpi", "noseries!", raise_error=False
        ).dict()
        com = self.com_api.get_unified_series(
            "usgdp", "uscpi", "noseries!", raise_error=False
        ).dict()

        comper_unified_dict(self, web, com)

    def test_get_unified_series_data_frame(self) -> None:
        web = self.web_api.get_unified_series(
            "usgdp",
            "uscpi",
        ).data_frame()
        com = self.com_api.get_unified_series(
            "usgdp",
            "uscpi",
        ).data_frame()

        self.assertEqual(len(web.compare(com)), 0)

        web = self.web_api.get_unified_series(
            "usgdp", "uscpi", "noseries!", raise_error=False
        ).data_frame()
        com = self.com_api.get_unified_series(
            "usgdp", "uscpi", "noseries!", raise_error=False
        ).data_frame()

        self.assertEqual(len(web.compare(com)), 0)


class Web(TestCase):
    def test_get_one_series(self) -> None:
        get_one_series(self, self.web_api)

    def test_get_series(self) -> None:
        get_series(self, self.web_api)

    def test_get_one_entity(self) -> None:
        get_one_entity(self, self.web_api)

    def test_get_entities(self) -> None:
        get_entities(self, self.web_api)

    def test_get_unified_series(self) -> None:
        get_unified_series(self, self.web_api)

    def test_get_unified_series_use_twice(self) -> None:
        get_unified_series_use_twice(self.web_api)

    def test_get_unified_series_no_series(self) -> None:
        get_unified_series_no_series(self, self.web_api)


class Com(TestCase):
    def test_get_one_series(self) -> None:
        get_one_series(self, self.com_api)

    def test_get_series(self) -> None:
        get_series(self, self.com_api)

    def test_get_one_entity(self) -> None:
        get_one_entity(self, self.com_api)

    def test_get_entities(self) -> None:
        get_entities(self, self.com_api)

    def test_get_unified_series(self) -> None:
        get_unified_series(self, self.com_api)

    def test_get_unified_series_use_twice(self) -> None:
        get_unified_series_use_twice(self.com_api)

    def test_get_unified_series_no_series(self) -> None:
        get_unified_series_no_series(self, self.com_api)


def get_one_series(test: TestCase, api: Api) -> None:
    series = api.get_one_series("usgdp").object()
    test.assertFalse(series.is_error, "is_error")

    test.assertNotEqual(len(series.values), 0, "values")
    test.assertNotEqual(len(series.dates), 0, "dates")
    test.assertEqual(
        len(series.dates), len(series.values), "len(series.dates) = len(series.values)"
    )

    test.assertEqual(series.entity_type, "TimeSeries", "entity_type")

    series = api.get_one_series("noseries!", raise_error=False).object()
    test.assertTrue(series.is_error, "is_error")
    test.assertEqual(series.error_message, "Not found", "error_message")

    # test raise_get_entities_error=True

    with test.assertRaises(GetEntitiesError) as context:
        api.get_one_series("noseries!").object()

    test.assertEqual(
        "failed to retrieve:\n\tnoseries! error_message: Not found",
        context.exception.message,
    )

    # test data_frame()

    data_frame = api.get_one_series("usgdp").data_frame()
    test.assertEqual(len(data_frame.index), 1)

    # values_and_dates_as_data_frame

    data_frame = api.get_one_series("usgdp").values_and_dates_as_data_frame()
    test.assertNotEqual(len(data_frame.index), 0)

    # values_and_dates_as_data_frame Error

    data_frame = api.get_one_series(
        "noseries!", raise_error=False
    ).values_and_dates_as_data_frame()

    test.assertEqual(len(data_frame.index), 1)

    # dict

    dict_series = api.get_one_series("usgdp", raise_error=False).dict()

    test.assertEqual(dict_series["Name"], "usgdp")
    test.assertNotEqual(len(dict_series["Values"]), 0)
    test.assertNotEqual(len(dict_series["Dates"]), 0)

    # error dict

    dict_series = api.get_one_series("noseries!", raise_error=False).dict()

    test.assertDictEqual(
        dict_series, {"Name": "noseries!", "ErrorMessage": "Not found"}
    )


def get_series(test: TestCase, api: Api) -> None:
    series = api.get_series(
        "usgdp", "uscpi", "noseries!", raise_error=False
    ).list_of_objects()

    # test.assertEqual(series[0].name, 'usgdp', 'name')
    test.assertEqual(series[0].primary_name, "usnaac0169", "primary_name")
    test.assertFalse(series[0].is_error, "is_error")
    test.assertEqual(series[0].error_message, "", "error_message")

    # test.assertEqual(series[1].name, 'uscpi', 'name')
    test.assertEqual(series[1].primary_name, "uspric2156", "primary_name")
    test.assertFalse(series[1].is_error, "is_error")
    test.assertEqual(series[1].error_message, "", "error_message")

    # test.assertEqual(series[2].name, 'noseries!', 'name')
    # test.assertEqual(series[2].primary_name, '', 'primary_name')
    test.assertTrue(series[2].is_error, "is_error")
    test.assertEqual(series[2].error_message, "Not found", "error_message")

    # test raise_get_entities_error=True

    with test.assertRaises(GetEntitiesError) as context:
        api.get_series("usgdp", "noseries!").list_of_dicts()

    test.assertEqual(
        "failed to retrieve:\n\tnoseries! error_message: Not found",
        context.exception.message,
    )

    # test data_frame()

    data_frame = api.get_series("usgdp", "uscpi").data_frame()
    test.assertEqual(len(data_frame.index), 2)


def get_one_entity(test: TestCase, api: Api) -> None:
    entitie = api.get_one_entity("usgdp").object()
    # test.assertEqual(entitie.name, 'usgdp', 'name')
    test.assertEqual(entitie.primary_name, "usnaac0169", "primary_name")
    test.assertFalse(entitie.is_error, "is_error")
    test.assertEqual(entitie.error_message, "", "error_message")
    test.assertIsNotNone(entitie.metadata, "metadata")

    entitie = api.get_one_entity("noseries!", raise_error=False).object()
    # test.assertEqual(entitie.name, 'noseries!', 'name')
    test.assertTrue(entitie.is_error, "is_error")
    test.assertEqual(entitie.error_message, "Not found", "error_message")

    # test raise_get_entities_error=True

    with test.assertRaises(GetEntitiesError) as context:
        api.get_one_entity("noseries!").dict()

    test.assertEqual(
        "failed to retrieve:\n\tnoseries! error_message: Not found",
        context.exception.message,
    )

    # test data_frame()

    data_frame = api.get_one_entity("usgdp").data_frame()
    test.assertEqual(len(data_frame.index), 1)

    # dict

    dict_series = api.get_one_entity("usgdp", raise_error=False).dict()

    test.assertEqual(dict_series["Name"], "usgdp")

    # error dict

    dict_series = api.get_one_entity("noseries!", raise_error=False).dict()

    test.assertDictEqual(
        dict_series, {"Name": "noseries!", "ErrorMessage": "Not found"}
    )


def get_entities(test: TestCase, api: Api) -> None:
    series = api.get_entities(
        "usgdp", "uscpi", "noseries!", raise_error=False
    ).list_of_objects()

    # test.assertEqual(series[0].name, 'usgdp', 'name')
    test.assertEqual(series[0].primary_name, "usnaac0169", "primary_name")
    test.assertFalse(series[0].is_error, "is_error")
    test.assertEqual(series[0].error_message, "", "error_message")

    # test.assertEqual(series[1].name, 'uscpi', 'name')
    test.assertEqual(series[1].primary_name, "uspric2156", "primary_name")
    test.assertFalse(series[1].is_error, "is_error")
    test.assertEqual(series[1].error_message, "", "error_message")

    # test.assertEqual(series[2].name, 'noseries!', 'name')
    # test.assertEqual(series[2].primary_name, '', 'primary_name')
    test.assertTrue(series[2].is_error, "is_error")
    test.assertEqual(series[2].error_message, "Not found", "error_message")

    # test raise_get_entities_error=True

    with test.assertRaises(GetEntitiesError) as context:
        api.get_entities("usgdp", "noseries!").list_of_dicts()

    test.assertEqual(
        "failed to retrieve:\n\tnoseries! error_message: Not found",
        context.exception.message,
    )

    # test data_frame()

    data_frame = api.get_entities("usgdp", "uscpi").data_frame()
    test.assertEqual(len(data_frame.index), 2)


def get_unified_series(test: TestCase, api: Api) -> None:
    unified = api.get_unified_series(
        SeriesEntry("usgdp"),
        SeriesEntry("uscpi"),
        "usgdp",
        "uscpi",
        SeriesEntry(
            "noseries!",
            missing_value_method=SeriesMissingValueMethod.PREVIOUS_VALUE,
        ),
        start_point=StartOrEndPoint.point_in_time(1989, 2, 1),
        end_point=StartOrEndPoint.point_in_time(datetime(2000, 2, 1)),
        raise_error=False,
    ).object()

    test.assertEqual(
        str(unified), "UnifiedSeries of 5 series", "__str__() or str(series)"
    )

    test.assertEqual(unified.__repr__(), "UnifiedSeries of 5 series", "__repr__")

    test.assertNotEqual(len(unified.dates), 0, "len(unified.dates)")

    for i in range(0, 4):
        test.assertEqual(
            len(unified.dates),
            len(unified[i].values),
            f"len(unified.dates) == len(unified[{i}].values)",
        )

        test.assertFalse(unified[i].is_error, f"is_error i = {i}")
        test.assertEqual(unified[i].error_message, "", f"error_message i = {i}")

        test.assertFalse(unified[i].is_error, f"is_error i = {i}")
        test.assertEqual(unified[i].error_message, "", f"error_message i = {i}")

    test.assertTrue(unified[4].is_error, "is_error")
    test.assertEqual(unified[4].error_message, "noseries! : Not found", "error_message")
    test.assertEqual(len(unified[4].values), 0, "len(unified[4].values)")

    data_frame = api.get_unified_series(
        "cyinea0001",
        "cypric0014",
        "cytour0076",
        "un_myos_cy_total",
        frequency=SeriesFrequency.ANNUAL,
        currency="USD",
        start_point=StartOrEndPoint.data_in_all_series(),
        end_point=StartOrEndPoint.data_in_all_series(),
    ).data_frame(
        [
            "dates",
            "Wage Growth",
            "CPI",
            "Income from Foreign Tourism",
            "Mean Years of Schooling",
        ]
    )

    ...


def get_unified_series_use_twice(api: Api) -> None:
    unified_return = api.get_unified_series(
        SeriesEntry("usgdp"),
        SeriesEntry("uscpi"),
    )

    unified_return.object()
    unified_return.object()


def get_unified_series_no_series(test: TestCase, api: Api) -> None:
    unified = api.get_unified_series(
        "noseries!",
        raise_error=False,
    ).object()

    test.assertEqual(unified.dates, tuple())
    test.assertEqual(len(unified.series), 1)
    test.assertEqual(len(unified), 1)

    test.assertEqual(unified[0].is_error, True)
    test.assertEqual(unified[0].error_message, "noseries! : Not found")
    test.assertEqual(unified[0].values, tuple())

    unified = api.get_unified_series(
        raise_error=False,
    ).object()

    test.assertEqual(unified.dates, tuple())
    test.assertEqual(len(unified.series), 0)
    test.assertEqual(len(unified), 0)

    with test.assertRaises(GetEntitiesError) as context:
        unified = api.get_unified_series("noseries!").object()

    test.assertEqual(
        "failed to retrieve:\n\tnoseries! error_message: noseries! : Not found",
        context.exception.message,
    )

    with test.assertRaises(GetEntitiesError) as context:
        api.get_unified_series("noseries!").dict()

    test.assertEqual(
        "failed to retrieve:\n\tnoseries! error_message: noseries! : Not found",
        context.exception.message,
    )
