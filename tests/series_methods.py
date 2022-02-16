# -*- coding: utf-8 -*-

from datetime import datetime

from macrobond_financial.common import Api, SeriesEntrie, StartOrEndPoint
from macrobond_financial.common.enums import SeriesFrequency, SeriesWeekdays, \
    SeriesMissingValueMethod

from tests.test_common import TestCase


class Common(TestCase):

    def test_get_one_series(self) -> None:
        series1 = self.web_api.series.get_one_series('usgdp')
        series2 = self.com_api.series.get_one_series('usgdp')

        self.assertAttributs(
            series1, series2,
            ['metadata', 'get_index_at_date', 'get_value_at_date']
        )

        self.assertEqual(
            series1.metadata['Description'],
            series2.metadata['Description'],
            'metadata[\'Description\']'
        )

        self.assertNotEqual(
            series1.metadata['LastModifiedTimeStamp'],
            series2.metadata['LastModifiedTimeStamp'],
            'metadata[\'LastModifiedTimeStamp\']'
        )

        self.assertEqual(
            series1.get_value_at_date(series1.start_date),
            series2.get_value_at_date(series2.start_date),
            'series.get_value_at_date(series.start_date)'
        )

        self.assertEqual(
            series1.get_value_at_date(series1.end_date),
            series2.get_value_at_date(series2.end_date),
            'series.get_value_at_date(series.end_date)'
        )

    def test_get_one_entitie(self) -> None:
        entitie1 = self.web_api.series.get_one_entitie('usgdp')
        entitie2 = self.com_api.series.get_one_entitie('usgdp')

        self.assertAttributs(
            entitie1, entitie2,
            ['metadata', 'get_index_at_date', 'get_value_at_date']
        )

        self.assertEqual(
            entitie1.metadata['Description'],
            entitie2.metadata['Description'],
            'metadata[\'Description\']'
        )


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


def get_one_series(test: TestCase, api: Api) -> None:
    series = api.series.get_one_series('usgdp')

    test.assertEqual(str(series), 'usgdp', 'str(series)')

    test.assertNotEqual(len(series.values), 0, 'values')
    test.assertIsNotNone(series.start_date, 'start_date')
    test.assertIsNotNone(series.end_date, 'end_date')
    test.assertEqual(series.frequency, SeriesFrequency.QUARTERLY, 'frequency')
    test.assertEqual(series.weekdays, SeriesWeekdays.FULL_WEEK, 'weekdays')

    series = api.series.get_one_series('noseries!')
    test.assertTrue(series.is_error, 'is_error')
    test.assertEqual(series.error_message, 'Not found', 'error_message')


def get_series(test: TestCase, api: Api) -> None:
    series = api.series.get_series('usgdp', 'uscpi', 'noseries!')

    test.assertEqual(series[0].name, 'usgdp', 'name')
    test.assertEqual(series[0].primary_name, 'usnaac0169', 'primary_name')
    test.assertFalse(series[0].is_error, 'is_error')
    test.assertEqual(series[0].error_message, '', 'error_message')

    test.assertEqual(series[1].name, 'uscpi', 'name')
    test.assertEqual(series[1].primary_name, 'uspric2156', 'primary_name')
    test.assertFalse(series[1].is_error, 'is_error')
    test.assertEqual(series[1].error_message, '', 'error_message')

    test.assertEqual(series[2].name, 'noseries!', 'name')
    test.assertEqual(series[2].primary_name, '', 'primary_name')
    test.assertTrue(series[2].is_error, 'is_error')
    test.assertEqual(series[2].error_message, 'Not found', 'error_message')


def get_one_entitie(test: TestCase, api: Api) -> None:
    entitie = api.series.get_one_entitie('usgdp')
    test.assertEqual(entitie.name, 'usgdp', 'name')
    test.assertEqual(entitie.primary_name, 'usnaac0169', 'primary_name')
    test.assertFalse(entitie.is_error, 'is_error')
    test.assertEqual(entitie.error_message, '', 'error_message')
    test.assertIsNotNone(entitie.metadata, 'metadata')

    entitie = api.series.get_one_entitie('noseries!')
    test.assertEqual(entitie.name, 'noseries!', 'name')
    test.assertTrue(entitie.is_error, 'is_error')
    test.assertEqual(entitie.error_message, 'Not found', 'error_message')


def get_entities(test: TestCase, api: Api) -> None:
    series = api.series.get_entities('usgdp', 'uscpi', 'noseries!')

    test.assertEqual(series[0].name, 'usgdp', 'name')
    test.assertEqual(series[0].primary_name, 'usnaac0169', 'primary_name')
    test.assertFalse(series[0].is_error, 'is_error')
    test.assertEqual(series[0].error_message, '', 'error_message')

    test.assertEqual(series[1].name, 'uscpi', 'name')
    test.assertEqual(series[1].primary_name, 'uspric2156', 'primary_name')
    test.assertFalse(series[1].is_error, 'is_error')
    test.assertEqual(series[1].error_message, '', 'error_message')

    test.assertEqual(series[2].name, 'noseries!', 'name')
    test.assertEqual(series[2].primary_name, '', 'primary_name')
    test.assertTrue(series[2].is_error, 'is_error')
    test.assertEqual(series[2].error_message, 'Not found', 'error_message')


def get_unified_series(test: TestCase, api: Api) -> None:
    series = api.series.get_unified_series(
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
    )

    # StartOrEndPoint.relative_to_observations(-1)
    # StartOrEndPoint.relative_to_quarters(-1)

    test.assertEqual(series[0].name, 'usgdp', 'name')
    test.assertEqual(series[0].primary_name, 'usnaac0169', 'primary_name')
    test.assertFalse(series[0].is_error, 'is_error')
    test.assertEqual(series[0].error_message, '', 'error_message')

    test.assertEqual(series[1].name, 'uscpi', 'name')
    test.assertEqual(series[1].primary_name, 'uspric2156', 'primary_name')
    test.assertFalse(series[1].is_error, 'is_error')
    test.assertEqual(series[1].error_message, '', 'error_message')

    test.assertEqual(series[2].name, 'usgdp', 'name')

    test.assertEqual(series[3].name, 'uscpi', 'name')

    test.assertEqual(series[4].name, 'noseries!', 'name')
    test.assertEqual(series[4].primary_name, '', 'primary_name')
    test.assertTrue(series[4].is_error, 'is_error')
    test.assertEqual(series[4].error_message, 'noseries! : Not found', 'error_message')

    test.assertIsNotNone(series[0].values, 'series[0].values')
    test.assertIsNotNone(series[1].values, 'series[1].values')
