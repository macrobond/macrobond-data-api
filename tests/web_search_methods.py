# -*- coding: utf-8 -*-

from tests.test_common import TestCase


class WebSearchMethods(TestCase):

    def test_web_entities_for_display(self) -> None:
        actual = self.web_api.session.search.entities_for_display({
            'filters': [{
                'text': "abc",
            }],
            'attributesForDisplayFormat': ['Name', 'Class'],
        })

        self.assertNotEqual(len(actual['results']), 0, "len(actual['results'])")

        self.assertTrue('Name' in actual['results'][0])
        self.assertTrue('Title' in actual['results'][0])
        self.assertTrue('Class' in actual['results'][0])

    def test_web_filter_lists(self) -> None:
        self.web_api.session.search.filter_lists('*')

    def test_web_get_entities(self) -> None:
        actual = self.web_api.session.search.get_entities(text='abc')

        self.assertNotEqual(len(actual['results']), 0, "len(actual['results'])")

        self.assertTrue('Name' in actual['results'][0])
