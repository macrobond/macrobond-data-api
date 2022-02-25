# -*- coding: utf-8 -*-

from datetime import datetime

from macrobond_financial.common import Api, SeriesEntrie, StartOrEndPoint
from macrobond_financial.common.enums import SeriesMissingValueMethod

from tests.test_common import TestCase


class Common(TestCase):

    def test_get_one_series(self) -> None:
        web = self.web_api.series.get_one_series('usgdp').object()
        com = self.com_api.series.get_one_series('usgdp').object()

        # intersection = [
        #     value for value in web.metadata.keys()
        #     if value in com.metadata.keys()
        # ]

        # for key in intersection:
        #     self.assertEqual(
        #         web.metadata[key], com.metadata[key], 'metadata key = ' + key
        #     )

        self.assertEqual(web.name, com.name, 'name')
        self.assertEqual(web.primary_name, com.primary_name, 'primary_name')
        self.assertEqual(web.title, com.title, 'title')
        self.assertEqual(web.entity_type, com.entity_type, 'entity_type')
        self.assertEqual(web.error_message, com.error_message, 'error_message')
        self.assertEqual(web.is_error, com.is_error, 'is_error')
        self.assertEqual(str(web), com.__str__(), '__str__() or str(series)')
        self.assertEqual(web.__repr__(), com.__repr__(), '__repr__')
        self.assertSequenceEqual(web.values, com.values, 'values')
        self.assertSequenceEqual(web.dates, com.dates, 'dates')

    def test_get_one_entitie(self) -> None:
        web = self.web_api.series.get_one_entitie('usgdp').object()
        com = self.com_api.series.get_one_entitie('usgdp').object()

        self.assertEqual(web.name, com.name, 'name')
        self.assertEqual(web.primary_name, com.primary_name, 'primary_name')
        self.assertEqual(web.title, com.title, 'title')
        self.assertEqual(web.entity_type, com.entity_type, 'entity_type')
        self.assertEqual(web.error_message, com.error_message, 'error_message')
        self.assertEqual(web.is_error, com.is_error, 'is_error')
        self.assertEqual(str(web), com.__str__(), '__str__() or str(series)')
        self.assertEqual(web.__repr__(), com.__repr__(), '__repr__')


class Web(TestCase):

    def test_get_one_series(self) -> None:
        get_one_series(self, self.web_api)

    def test_get_series(self) -> None:
        get_series(self, self.web_api)

    def test_get_one_entitie(self) -> None:
        get_one_entitie(self, self.web_api)

    def test_get_entities(self) -> None:
        get_entities(self, self.web_api)

    def test_get_unified_series(self) -> None:
        get_unified_series(self, self.web_api)

    def test_get_unified_series_use_twice(self) -> None:
        get_unified_series_use_twice(self.web_api)


class Com(TestCase):

    def test_get_one_series(self) -> None:
        get_one_series(self, self.com_api)

    def test_get_series(self) -> None:
        get_series(self, self.com_api)

    def test_get_one_entitie(self) -> None:
        get_one_entitie(self, self.com_api)

    def test_get_entities(self) -> None:
        get_entities(self, self.com_api)

    def test_get_unified_series(self) -> None:
        get_unified_series(self, self.com_api)

    def test_get_unified_series_use_twice(self) -> None:
        get_unified_series_use_twice(self.com_api)


def get_one_series(test: TestCase, api: Api) -> None:
    series = api.series.get_one_series('usgdp').object()
    test.assertFalse(series.is_error, 'is_error')

    test.assertNotEqual(len(series.values), 0, 'values')
    test.assertNotEqual(len(series.dates), 0, 'dates')
    test.assertEqual(
        len(series.dates), len(series.values), 'len(series.dates) = len(series.values)'
    )

    test.assertEqual(series.entity_type, 'TimeSeries', 'entity_type')

    series = api.series.get_one_series('noseries!').object()
    test.assertTrue(series.is_error, 'is_error')
    test.assertEqual(series.error_message, 'Not found', 'error_message')


def get_series(test: TestCase, api: Api) -> None:
    series = api.series.get_series('usgdp', 'uscpi', 'noseries!').tuple_of_objects()

    # test.assertEqual(series[0].name, 'usgdp', 'name')
    test.assertEqual(series[0].primary_name, 'usnaac0169', 'primary_name')
    test.assertFalse(series[0].is_error, 'is_error')
    test.assertEqual(series[0].error_message, '', 'error_message')

    # test.assertEqual(series[1].name, 'uscpi', 'name')
    test.assertEqual(series[1].primary_name, 'uspric2156', 'primary_name')
    test.assertFalse(series[1].is_error, 'is_error')
    test.assertEqual(series[1].error_message, '', 'error_message')

    # test.assertEqual(series[2].name, 'noseries!', 'name')
    # test.assertEqual(series[2].primary_name, '', 'primary_name')
    test.assertTrue(series[2].is_error, 'is_error')
    test.assertEqual(series[2].error_message, 'Not found', 'error_message')


def get_one_entitie(test: TestCase, api: Api) -> None:
    entitie = api.series.get_one_entitie('usgdp').object()
    # test.assertEqual(entitie.name, 'usgdp', 'name')
    test.assertEqual(entitie.primary_name, 'usnaac0169', 'primary_name')
    test.assertFalse(entitie.is_error, 'is_error')
    test.assertEqual(entitie.error_message, '', 'error_message')
    test.assertIsNotNone(entitie.metadata, 'metadata')

    entitie = api.series.get_one_entitie('noseries!').object()
    # test.assertEqual(entitie.name, 'noseries!', 'name')
    test.assertTrue(entitie.is_error, 'is_error')
    test.assertEqual(entitie.error_message, 'Not found', 'error_message')


def get_entities(test: TestCase, api: Api) -> None:
    series = api.series.get_entities('usgdp', 'uscpi', 'noseries!').tuple_of_objects()

    # test.assertEqual(series[0].name, 'usgdp', 'name')
    test.assertEqual(series[0].primary_name, 'usnaac0169', 'primary_name')
    test.assertFalse(series[0].is_error, 'is_error')
    test.assertEqual(series[0].error_message, '', 'error_message')

    # test.assertEqual(series[1].name, 'uscpi', 'name')
    test.assertEqual(series[1].primary_name, 'uspric2156', 'primary_name')
    test.assertFalse(series[1].is_error, 'is_error')
    test.assertEqual(series[1].error_message, '', 'error_message')

    # test.assertEqual(series[2].name, 'noseries!', 'name')
    # test.assertEqual(series[2].primary_name, '', 'primary_name')
    test.assertTrue(series[2].is_error, 'is_error')
    test.assertEqual(series[2].error_message, 'Not found', 'error_message')


def get_unified_series(test: TestCase, api: Api) -> None:
    unified = api.series.get_unified_series(
        SeriesEntrie('usgdp'),
        SeriesEntrie('uscpi'),
        'usgdp',
        'uscpi',
        SeriesEntrie(
            'noseries!',
            missing_value_method=SeriesMissingValueMethod.PREVIOUS_VALUE,
        ),
        start_point=StartOrEndPoint.point_in_time(1989, 2, 1),
        end_point=StartOrEndPoint.point_in_time(datetime(2000, 2, 1))
    ).object()

    test.assertEqual(str(unified), 'UnifiedSeries of 5 series', '__str__() or str(series)')

    test.assertEqual(unified.__repr__(), 'UnifiedSeries of 5 series', '__repr__')

    test.assertNotEqual(len(unified.dates), 0, 'len(unified.dates)')

    for i in range(0, 4):
        test.assertEqual(
            len(unified.dates), len(unified[i].values),
            f'len(unified.dates) == len(unified[{i}].values)'
        )

        test.assertFalse(unified[i].is_error, f'is_error i = {i}')
        test.assertEqual(unified[i].error_message, '', f'error_message i = {i}')

        test.assertFalse(unified[i].is_error, f'is_error i = {i}')
        test.assertEqual(unified[i].error_message, '', f'error_message i = {i}')

    test.assertTrue(unified[4].is_error, 'is_error')
    test.assertEqual(unified[4].error_message, 'noseries! : Not found', 'error_message')
    test.assertEqual(len(unified[4].values), 0, 'len(unified[4].values)')


def get_unified_series_use_twice(api: Api) -> None:
    unified_return = api.series.get_unified_series(
        SeriesEntrie('usgdp'),
        SeriesEntrie('uscpi'),
    )

    unified_return.object()
    unified_return.object()
