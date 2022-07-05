# -*- coding: utf-8 -*-
from typing import cast


from macrobond_financial.web.web_types import ProblemDetailsException
from macrobond_financial.common.types import SeriesEntry
from tests.test_common import TestCase


class WebErrorHandling(TestCase):
    def test_get_unified_series_error(self) -> None:
        with self.assertRaises(ProblemDetailsException) as context:
            self.web_api.get_unified_series(SeriesEntry(name=cast(str, 1)))

        if context.exception.errors is None:
            self.fail("context.exception.errors is None")

        self.assertEqual(
            ["The request field is required."], context.exception.errors.get("request")
        )
