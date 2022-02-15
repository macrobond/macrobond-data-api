# -*- coding: utf-8 -*-

from datetime import datetime

from macrobond_financial.common import Api, SeriesEntrie, StartOrEndPoint
from macrobond_financial.common.enums import SeriesFrequency, SeriesWeekdays, \
    SeriesMissingValueMethod

from tests.test_common import TestCase


class SeriesMethods(TestCase):

    #  get_one_series

    def test_web_get_one_series(self) -> None:
        self.__get_one_series(self.web_api)

    def test_com_get_one_series(self) -> None:
        self.__get_one_series(self.com_api)

    def __get_one_series(self, api: Api) -> None:
        series = api.series.get_one_series('usgdp')

        self.assertEqual(str(series), 'usgdp', 'str(series)')

        self.assertNotEqual(len(series.values), 0, 'values')
        self.assertIsNotNone(series.start_date, 'start_date')
        self.assertIsNotNone(series.end_date, 'end_date')
        self.assertEqual(series.frequency, SeriesFrequency.QUARTERLY, 'frequency')
        self.assertEqual(series.weekdays, SeriesWeekdays.FULL_WEEK, 'weekdays')

        series = api.series.get_one_series('noseries!')
        self.assertTrue(series.is_error, 'is_error')
        self.assertEqual(series.error_message, 'Not found', 'error_message')

    def test_get_one_series(self) -> None:
        series1 = self.web_api.series.get_one_series('usgdp')
        series2 = self.com_api.series.get_one_series('usgdp')

        self.assertAttributs(
            series1, series2,
            ['metadata', 'get_index_at_date', 'get_value_at_date']
        )
        self.assertAttributs(
            series1.metadata, series2.metadata,
            ['get_first_value', 'get_values', 'get_dict']
        )

        self.assertEqual(
            series1.metadata.get_dict()['Description'],
            series2.metadata.get_dict()['Description'],
            'metadata.get_dict()[\'Description\']'
        )

        self.assertNotEqual(
            series1.metadata.get_dict()['LastModifiedTimeStamp'],
            series2.metadata.get_dict()['LastModifiedTimeStamp'],
            'metadata.get_dict()[\'LastModifiedTimeStamp\']'
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

    def test_web_get_series(self) -> None:
        self.__get_series(self.web_api)

    def test_com_get_series(self) -> None:
        self.__get_series(self.com_api)

    def __get_series(self, api: Api) -> None:
        series = api.series.get_series('usgdp', 'uscpi', 'noseries!')

        self.assertEqual(series[0].name, 'usgdp', 'name')
        self.assertEqual(series[0].primary_name, 'usnaac0169', 'primary_name')
        self.assertFalse(series[0].is_error, 'is_error')
        self.assertEqual(series[0].error_message, '', 'error_message')

        self.assertEqual(series[1].name, 'uscpi', 'name')
        self.assertEqual(series[1].primary_name, 'uspric2156', 'primary_name')
        self.assertFalse(series[1].is_error, 'is_error')
        self.assertEqual(series[1].error_message, '', 'error_message')

        self.assertEqual(series[2].name, 'noseries!', 'name')
        self.assertEqual(series[2].primary_name, '', 'primary_name')
        self.assertTrue(series[2].is_error, 'is_error')
        self.assertEqual(series[2].error_message, 'Not found', 'error_message')

    #  get_one_entitie

    def test_web_get_one_entitie(self) -> None:
        self.__get_one_entitie(self.web_api)

    def test_com_get_one_entitie(self) -> None:
        self.__get_one_entitie(self.com_api)

    def __get_one_entitie(self, api: Api) -> None:
        entitie = api.series.get_one_entitie('usgdp')
        self.assertEqual(entitie.name, 'usgdp', 'name')
        self.assertEqual(entitie.primary_name, 'usnaac0169', 'primary_name')
        self.assertFalse(entitie.is_error, 'is_error')
        self.assertEqual(entitie.error_message, '', 'error_message')
        self.assertIsNotNone(entitie.metadata, 'metadata')

        entitie = api.series.get_one_entitie('noseries!')
        self.assertEqual(entitie.name, 'noseries!', 'name')
        self.assertTrue(entitie.is_error, 'is_error')
        self.assertEqual(entitie.error_message, 'Not found', 'error_message')

    def test_get_one_entitie(self) -> None:
        entitie1 = self.web_api.series.get_one_entitie('usgdp')
        entitie2 = self.com_api.series.get_one_entitie('usgdp')

        self.assertAttributs(
            entitie1, entitie2,
            ['metadata', 'get_index_at_date', 'get_value_at_date']
        )
        self.assertAttributs(
            entitie1.metadata, entitie2.metadata,
            ['get_first_value', 'get_values', 'get_dict']
        )

    # get_entities

    def test_web_get_entities(self) -> None:
        self.__get_entities(self.web_api)

    def test_com_get_entities(self) -> None:
        self.__get_entities(self.com_api)

    def __get_entities(self, api: Api) -> None:
        series = api.series.get_entities('usgdp', 'uscpi', 'noseries!')

        self.assertEqual(series[0].name, 'usgdp', 'name')
        self.assertEqual(series[0].primary_name, 'usnaac0169', 'primary_name')
        self.assertFalse(series[0].is_error, 'is_error')
        self.assertEqual(series[0].error_message, '', 'error_message')

        self.assertEqual(series[1].name, 'uscpi', 'name')
        self.assertEqual(series[1].primary_name, 'uspric2156', 'primary_name')
        self.assertFalse(series[1].is_error, 'is_error')
        self.assertEqual(series[1].error_message, '', 'error_message')

        self.assertEqual(series[2].name, 'noseries!', 'name')
        self.assertEqual(series[2].primary_name, '', 'primary_name')
        self.assertTrue(series[2].is_error, 'is_error')
        self.assertEqual(series[2].error_message, 'Not found', 'error_message')

    # get_unified_series

    def test_web_get_unified_series(self) -> None:
        self.__get_unified_series(self.web_api)

    def test_com_get_unified_series(self) -> None:
        self.__get_unified_series(self.com_api)

    def __get_unified_series(self, api: Api) -> None:
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

        self.assertEqual(series[0].name, 'usgdp', 'name')
        self.assertEqual(series[0].primary_name, 'usnaac0169', 'primary_name')
        self.assertFalse(series[0].is_error, 'is_error')
        self.assertEqual(series[0].error_message, '', 'error_message')

        self.assertEqual(series[1].name, 'uscpi', 'name')
        self.assertEqual(series[1].primary_name, 'uspric2156', 'primary_name')
        self.assertFalse(series[1].is_error, 'is_error')
        self.assertEqual(series[1].error_message, '', 'error_message')

        self.assertEqual(series[2].name, 'usgdp', 'name')

        self.assertEqual(series[3].name, 'uscpi', 'name')

        self.assertEqual(series[4].name, 'noseries!', 'name')
        self.assertEqual(series[4].primary_name, '', 'primary_name')
        self.assertTrue(series[4].is_error, 'is_error')
        self.assertEqual(series[4].error_message, 'noseries! : Not found', 'error_message')

        self.assertIsNotNone(series[0].values, 'series[0].values')
        self.assertIsNotNone(series[1].values, 'series[1].values')
