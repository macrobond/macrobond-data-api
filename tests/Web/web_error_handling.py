from typing import cast


import pytest
from macrobond_data_api.web.web_types import ProblemDetailsException
from macrobond_data_api.common.types import SeriesEntry

from macrobond_data_api.web import WebApi


def test_get_unified_series_error(web: WebApi) -> None:
    with pytest.raises(ProblemDetailsException) as ex:
        web.get_unified_series(SeriesEntry(name=cast(str, 1)))
    assert ex.value.errors["request"] == ["The request field is required."]  # type: ignore
