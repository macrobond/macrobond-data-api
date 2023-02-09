from pandas import Series as PdSeries, DataFrame  # type: ignore

from macrobond_data_api.common import Api
from macrobond_data_api.common.types import GetEntitiesError, SeriesEntry

from tests.test_common import TestCase


class Web(TestCase):
    def test_get_one_series(self) -> None:
        get_one_series(self, self.web_api)

    def test_get_series(self) -> None:
        get_series(self, self.web_api)

    def test_get_one_entity(self) -> None:
        get_one_entity(self, self.web_api)

    def test_get_entities(self) -> None:
        get_entities(self, self.web_api)

    def test_get_unified_series_no_series(self) -> None:
        get_unified_series_no_series(self, self.web_api)

    def test_get_unified_series_vintage(self) -> None:
        get_unified_series_vintage(self, self.web_api)


class Com(TestCase):
    def test_get_one_series(self) -> None:
        get_one_series(self, self.com_api)

    def test_get_series(self) -> None:
        get_series(self, self.com_api)

    def test_get_one_entity(self) -> None:
        get_one_entity(self, self.com_api)

    def test_get_entities(self) -> None:
        get_entities(self, self.com_api)

    def test_get_unified_series_no_series(self) -> None:
        get_unified_series_no_series(self, self.com_api)

    def test_get_unified_series_vintage(self) -> None:
        get_unified_series_vintage(self, self.com_api)


def get_one_series(test: TestCase, api: Api) -> None:
    series = api.get_one_series("usgdp")
    test.assertFalse(series.is_error, "is_error")

    test.assertNotEqual(len(series.values), 0, "values")
    test.assertNotEqual(len(series.dates), 0, "dates")
    test.assertEqual(len(series.dates), len(series.values), "len(series.dates) = len(series.values)")

    test.assertEqual(series.entity_type, "TimeSeries", "entity_type")

    test.assertEqual(float, type(series.values[0]))

    series = api.get_one_series("noseries!", raise_error=False)
    test.assertTrue(series.is_error, "is_error")
    test.assertEqual(series.error_message, "Not found", "error_message")

    # test raise_get_entities_error=True

    with test.assertRaises(GetEntitiesError) as context:
        api.get_one_series("noseries!")

    test.assertEqual(
        "failed to retrieve:\n\tnoseries! error_message: Not found",
        context.exception.message,
    )


def get_series(test: TestCase, api: Api) -> None:
    series = api.get_series("usgdp", "uscpi", "noseries!", raise_error=False)

    # test.assertEqual(series[0].name, 'usgdp', 'name')
    test.assertEqual(series[0].primary_name, "usnaac0169", "primary_name")
    test.assertFalse(series[0].is_error, "is_error")
    test.assertEqual(series[0].error_message, "", "error_message")
    test.assertEqual(float, type(series[0].values[0]))

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
        api.get_series("usgdp", "noseries!")

    test.assertEqual(
        "failed to retrieve:\n\tnoseries! error_message: Not found",
        context.exception.message,
    )


def get_one_entity(test: TestCase, api: Api) -> None:
    entitie = api.get_one_entity("usgdp")
    # test.assertEqual(entitie.name, 'usgdp', 'name')
    test.assertEqual(entitie.primary_name, "usnaac0169", "primary_name")
    test.assertFalse(entitie.is_error, "is_error")
    test.assertEqual(entitie.error_message, "", "error_message")
    test.assertIsNotNone(entitie.metadata, "metadata")

    entitie = api.get_one_entity("noseries!", raise_error=False)
    # test.assertEqual(entitie.name, 'noseries!', 'name')
    test.assertTrue(entitie.is_error, "is_error")
    test.assertEqual(entitie.error_message, "Not found", "error_message")

    # test raise_get_entities_error=True

    with test.assertRaises(GetEntitiesError) as context:
        api.get_one_entity("noseries!")

    test.assertEqual(
        "failed to retrieve:\n\tnoseries! error_message: Not found",
        context.exception.message,
    )

    # dict

    dict_series = api.get_one_entity("usgdp", raise_error=False).to_dict()

    test.assertEqual(dict_series["Name"], "usgdp")
    test.assertEqual(dict_series["metadata.Class"], "stock")

    # test is_discontinued

    test.assertTrue(api.get_one_entity("uslama9621").is_discontinued)

    test.assertFalse(api.get_one_entity("usgdp").is_discontinued)


def get_entities(test: TestCase, api: Api) -> None:
    entities = api.get_entities("usgdp", "uscpi", "noseries!", raise_error=False)

    # test.assertEqual(series[0].name, 'usgdp', 'name')
    test.assertEqual(entities[0].primary_name, "usnaac0169", "primary_name")
    test.assertFalse(entities[0].is_error, "is_error")
    test.assertEqual(entities[0].error_message, "", "error_message")

    # test.assertEqual(series[1].name, 'uscpi', 'name')
    test.assertEqual(entities[1].primary_name, "uspric2156", "primary_name")
    test.assertFalse(entities[1].is_error, "is_error")
    test.assertEqual(entities[1].error_message, "", "error_message")

    # test.assertEqual(series[2].name, 'noseries!', 'name')
    # test.assertEqual(series[2].primary_name, '', 'primary_name')
    test.assertTrue(entities[2].is_error, "is_error")
    test.assertEqual(entities[2].error_message, "Not found", "error_message")

    # test raise_get_entities_error=True

    with test.assertRaises(GetEntitiesError) as context:
        api.get_entities("usgdp", "noseries!")

    test.assertEqual(
        "failed to retrieve:\n\tnoseries! error_message: Not found",
        context.exception.message,
    )


def get_unified_series_no_series(test: TestCase, api: Api) -> None:
    unified = api.get_unified_series(
        "noseries!",
        raise_error=False,
    )

    test.assertEqual(unified.dates, tuple())
    test.assertEqual(len(unified), 1)

    test.assertEqual(unified[0].is_error, True)
    test.assertEqual(unified[0].error_message, "noseries! : Not found")
    test.assertEqual(unified[0].values, tuple())

    unified = api.get_unified_series(
        raise_error=False,
    )

    test.assertEqual(unified.dates, tuple())
    test.assertEqual(len(unified), 0)

    with test.assertRaises(GetEntitiesError) as context:
        unified = api.get_unified_series("noseries!")

    test.assertEqual(
        "failed to retrieve:\n\tnoseries! error_message: noseries! : Not found",
        context.exception.message,
    )


def get_unified_series_vintage(test: TestCase, api: Api) -> None:
    revision_info = api.get_revision_info("usgdp")[0]

    unified_1 = api.get_unified_series(SeriesEntry("usgdp"))[0]

    unified_2 = api.get_unified_series(SeriesEntry("usgdp", revision_info.time_stamp_of_last_revision))[0]

    unified_3 = api.get_unified_series(SeriesEntry("usgdp", revision_info.time_stamp_of_first_revision))[0]

    test.assertEqual(unified_1.values, unified_2.values)

    test.assertNotEqual(unified_1.values, unified_3.values)


class Common(TestCase):
    # get_one_series

    def test_get_one_series_values_to_pd_series(self) -> None:
        self.assertEqual(
            0,
            len(
                PdSeries.compare(
                    self.web_api.get_one_series("usgdp").values_to_pd_series(),
                    self.com_api.get_one_series("usgdp").values_to_pd_series(),
                )
            ),
            "usgdp",
        )
        self.assertEqual(
            0,
            len(
                PdSeries.compare(
                    self.web_api.get_one_series("ustrad4488").values_to_pd_series(),
                    self.com_api.get_one_series("ustrad4488").values_to_pd_series(),
                )
            ),
            "ustrad4488",
        )
        self.assertEqual(
            0,
            len(
                PdSeries.compare(
                    self.web_api.get_one_series("ct_au_e_ao_c_22_v").values_to_pd_series(),
                    self.com_api.get_one_series("ct_au_e_ao_c_22_v").values_to_pd_series(),
                )
            ),
            "ct_au_e_ao_c_22_v",
        )

    # get_unified_series

    def test_get_unified_series_to_pd_data_frame(self) -> None:
        self.assertEqual(
            0,
            len(
                DataFrame.compare(
                    self.web_api.get_unified_series("usgdp").to_pd_data_frame(),
                    self.com_api.get_unified_series("usgdp").to_pd_data_frame(),
                )
            ),
            "usgdp",
        )
        self.assertEqual(
            0,
            len(
                DataFrame.compare(
                    self.web_api.get_unified_series("ustrad4488").to_pd_data_frame(),
                    self.com_api.get_unified_series("ustrad4488").to_pd_data_frame(),
                )
            ),
            "ustrad4488",
        )
        self.assertEqual(
            0,
            len(
                DataFrame.compare(
                    self.web_api.get_unified_series("ct_au_e_ao_c_22_v").to_pd_data_frame(),
                    self.com_api.get_unified_series("ct_au_e_ao_c_22_v").to_pd_data_frame(),
                )
            ),
            "ct_au_e_ao_c_22_v",
        )
