# -*- coding: utf-8 -*-

from macrobond_financial.common import Api, SearchFilter, StartOrEndPoint

from tests.test_common import TestCase


class SearchMethods(TestCase):

    #  search

    def test_web_search(self) -> None:
        self.__search(self.web_api)

    def test_com_search(self) -> None:
        self.__search(self.com_api)

    def __search(self, api: Api) -> None:
        search_result = api.search.search(text="usgdp")

        self.assertNotEqual(len(search_result.entities), 0, 'len(search_result.entities) != 0')
        first = search_result.entities[0]

        self.assertNotEqual(
            len(first.metadata.get_dict()), 0,
            'len(first.metadata.get_dict()) != 0'
        )

    # multi_filter

    def test_web_series_multi_filter(self) -> None:
        self.__series_multi_filter(self.web_api)

    def test_com_series_multi_filter(self) -> None:
        self.__series_multi_filter(self.com_api)

    def __series_multi_filter(self, api: Api) -> None:
        search_result = api.search.series_multi_filter(SearchFilter(text="usgdp"))

        self.assertNotEqual(len(search_result.entities), 0, 'len(search_result.entities) != 0')
        first = search_result.entities[0]

        self.assertNotEqual(
            len(first.metadata.get_dict()), 0,
            'len(first.metadata.get_dict()) != 0'
        )

    def test_series_multi_filter(self) -> None:
        com = self.com_api.search.series_multi_filter(SearchFilter(text="usgdp"))
        web = self.web_api.search.series_multi_filter(SearchFilter(text="usgdp"))

        self.assertEqual(
            len(com.entities), len(web.entities),
            'len(com.entities) == len(web.entities)'
        )

        self.assertNotEqual(len(com.entities), 0, 'len(com.entities) != 0')

        com_first = com.entities[0]
        web_first = web.entities[0]

        self.assertEqual(str(com_first), str(web_first), '__str__()')
        # self.assertEqual(com_first.__repr__(), web_first.__repr__(), '__repr__()')
        self.assertEqual(com_first.name, web_first.name, 'name')
        self.assertEqual(com_first.primary_name, web_first.primary_name, 'primary_name')
        self.assertEqual(com_first.title, web_first.title, 'title')
        self.assertEqual(com_first.is_error, web_first.is_error, 'is_error')
        self.assertEqual(com_first.error_message, web_first.error_message, 'error_message')

    # must_have_attributes

    def test_web_series_multi_filter_must_have_attributes(self) -> None:
        self.__series_multi_filter_must_have_attributes(self.web_api)

    def test_com_series_multi_filter_must_have_attributes(self) -> None:
        self.__series_multi_filter_must_have_attributes(self.com_api)

    def __series_multi_filter_must_have_attributes(self, api: Api) -> None:
        search_result = api.search.series_multi_filter(
            SearchFilter(must_have_attributes=["MoveBase"])
        )

        self.assertNotEqual(len(search_result.entities), 0, 'len(com.entities) != 0')

        for entitie in search_result.entities:
            if 'MoveBase' not in entitie.metadata.get_dict():
                self.fail('MoveBase not in ' + entitie.name)

    # must_not_have_attributes

    def test_web_series_multi_filter_must_not_have_attributes(self) -> None:
        self.__series_multi_filter_must_not_have_attributes(self.web_api)

    def test_com_series_multi_filter_must_not_have_attributes(self) -> None:
        self.__series_multi_filter_must_not_have_attributes(self.com_api)

    def __series_multi_filter_must_not_have_attributes(self, api: Api) -> None:
        search_result = api.search.series_multi_filter(
            SearchFilter(must_not_have_attributes=["MoveBase"])
        )

        self.assertNotEqual(len(search_result.entities), 0, 'len(com.entities) != 0')

        for entitie in search_result.entities:
            if 'MoveBase' in entitie.metadata.get_dict():
                self.fail('MoveBase is in ' + entitie.name)

    # must_have_values

    def test_web_series_multi_filter_must_have_values(self) -> None:
        self.__series_multi_filter_must_have_values(self.web_api)

    def test_com_series_multi_filter_must_have_values(self) -> None:
        self.__series_multi_filter_must_have_values(self.com_api)

    def __series_multi_filter_must_have_values(self, api: Api) -> None:
        search_result = api.search.series_multi_filter(
            SearchFilter(must_have_values={"MoveBase": 'pp100'})
        )

        self.assertNotEqual(len(search_result.entities), 0, 'len(com.entities) != 0')

        for entitie in search_result.entities:
            self.assertEqual(
                entitie.metadata.get_dict().get('MoveBase'),
                'pp100',
                'MoveBase != "pp100" ' + entitie.name
            )

    # must_not_have_values

    def test_web_series_multi_filter_must_not_have_values(self) -> None:
        self.__series_multi_filter_must_not_have_values(self.web_api)

    def test_com_series_multi_filter_must_not_have_values(self) -> None:
        self.__series_multi_filter_must_not_have_values(self.com_api)

    def __series_multi_filter_must_not_have_values(self, api: Api) -> None:
        search_result = api.search.series_multi_filter(
            SearchFilter(must_not_have_values={"MoveBase": 'pp100'})
        )

        self.assertNotEqual(len(search_result.entities), 0, 'len(com.entities) != 0')

        for entitie in search_result.entities:
            self.assertNotEqual(
                entitie.metadata.get_dict().get('MoveBase'),
                'pp100',
                'MoveBase == "pp100" ' + entitie.name
            )

    # include_discontinued

    def test_web_series_multi_filter_include_discontinued(self) -> None:
        self.__series_multi_filter_include_discontinued(self.web_api)

    def test_com_series_multi_filter_include_discontinued(self) -> None:
        self.__series_multi_filter_include_discontinued(self.com_api)

    def __series_multi_filter_include_discontinued(self, api: Api) -> None:
        text = 's_07707'

        include = api.search.series_multi_filter(
            SearchFilter(text=text),
            include_discontinued=True,
        )

        not_include = api.search.series_multi_filter(
            SearchFilter(text=text),
            include_discontinued=False,
        )

        self.assertNotEqual(len(include), 6000, 'len(include) != 6000')
        self.assertNotEqual(len(not_include), 6000, 'len(not_include) != 6000')

        self.assertNotEqual(len(include), 0, 'len(include) != 0')
        self.assertNotEqual(len(not_include), 0, 'len(not_include) != 0')

        self.assertGreater(len(include), len(not_include), 'include > not_include')

    # entity_types

    def test_web_series_multi_filter_entity_types(self) -> None:
        self.__series_multi_filter_entity_types(self.web_api)

    def test_com_series_multi_filter_entity_types(self) -> None:
        self.__series_multi_filter_entity_types(self.com_api)

    def __series_multi_filter_entity_types(self, api: Api) -> None:
        text = 'abc'

        security = api.search.series_multi_filter(
            SearchFilter(text=text, entity_types=['Security'])
        )

        self.assertNotEqual(len(security), 0, 'len(security) != 0')

        for entitie in security.entities:
            self.assertEqual(
                entitie.entity_type, 'Security', 'EntityType != "Security" ' + entitie.name
            )

    # StartOrEndPoint

    def test_start_or_end_point(self) -> None:

        self.assertEqual(
            StartOrEndPoint.relative_to_observations(-1).__repr__(),
            '-1 mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.relative_to_observations(-1).__repr__()'
        )

        self.assertEqual(
            str(StartOrEndPoint.relative_to_observations(-1)),
            '-1 mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.relative_to_observations(-1).__str__()'
        )

        self.assertEqual(
            str(StartOrEndPoint.relative_to_years(-1)),
            '-1y mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.relative_to_years(-1).__str__()'
        )

        self.assertEqual(
            str(StartOrEndPoint.relative_to_quarters(-1)),
            '-1q mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.relative_to_quarters(-1).__str__()'
        )

        self.assertEqual(
            str(StartOrEndPoint.relative_to_months(-1)),
            '-1m mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.relative_to_months(-1).__str__()'
        )

        self.assertEqual(
            str(StartOrEndPoint.relative_to_weeks(-1)),
            '-1w mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.relative_to_weeks(-1).__str__()'
        )

        self.assertEqual(
            str(StartOrEndPoint.relative_to_days(-1)),
            '-1d mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.relative_to_days(-1).__str__()'
        )

        self.assertEqual(
            str(StartOrEndPoint('-1', None)),
            '-1 mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            '(StartOrEndPoint(\'-1\', None).__str__()'
        )

        self.assertEqual(
            str(StartOrEndPoint.data_in_all_series()),
            ' mode:CalendarDateMode.DATA_IN_ALL_SERIES',
            'StartOrEndPoint.data_in_all_series()'
        )

        self.assertEqual(
            str(StartOrEndPoint.data_in_any_series()),
            ' mode:CalendarDateMode.DATA_IN_ANY_SERIES',
            'StartOrEndPoint.data_in_any_series()'
        )
