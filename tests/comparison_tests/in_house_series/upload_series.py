from typing import Any
from datetime import datetime, timezone

import pytest

from macrobond_data_api.common import Api
from macrobond_data_api.common.types import Series
from macrobond_data_api.common.enums import SeriesFrequency

from macrobond_data_api.web import WebApi
from macrobond_data_api.com import ComApi


def _try_delete_series(api: Api, *names: str) -> None:
    for name in names:
        try:
            api.delete_serie(name)
        except:  # noqa: E722
            ...


@pytest.mark.usefixtures("lock_test")
def test_1(web: WebApi, com: ComApi, test_metadata: Any) -> None:
    web_name = "ih:mb:priv:test_name_py_web"
    com_name = "ih:mb:priv:test_name_py_com"

    _try_delete_series(web, web_name, com_name)

    def upload_and_get_series(api: Api, name: str) -> Series:
        api.upload_series(
            name,
            "test_description",
            "us",
            "test_category",
            SeriesFrequency.DAILY,
            [1.0, 2, 3.0],
            datetime(2020, 1, 1, tzinfo=timezone.utc),
        )

        return api.get_one_series(name)

    try:
        web_series = upload_and_get_series(web, web_name)
        com_series = upload_and_get_series(com, com_name)

        test_metadata(web_series, com_series, ignore_keys=["LastModifiedTimeStamp", "PrimName"])

        web_series.name = "test"
        com_series.name = "test"

        assert web_series == com_series

    finally:
        try:
            web.delete_serie(web_name)
        finally:
            com.delete_serie(com_name)


@pytest.mark.usefixtures("lock_test")
def test_2(web: WebApi, com: ComApi, test_metadata: Any) -> None:
    web_name = "ih:mb:priv:test_name_py_web"
    com_name = "ih:mb:priv:test_name_py_com"

    _try_delete_series(web, web_name, com_name)

    def upload_and_get_series(api: Api, name: str) -> Series:
        api.upload_series(
            name,
            "test_description",
            "us",
            "test_category",
            SeriesFrequency.DAILY,
            [1.0, 2, 3.0],
            datetime(2020, 1, 1, tzinfo=timezone.utc),
            # metadata={"RevisionHistorySourceCutOffDate": datetime(2021, 1, 1, tzinfo=timezone.utc)},
            forecast_flags=[True, False, True],
        )

        return api.get_one_series(name)

    try:
        com_series = upload_and_get_series(com, com_name)
        web_series = upload_and_get_series(web, web_name)

        test_metadata(web_series, com_series, ignore_keys=["LastModifiedTimeStamp", "PrimName"])

        web_series.name = "test"
        com_series.name = "test"

        assert web_series == com_series

    finally:
        try:
            web.delete_serie(web_name)
        finally:
            com.delete_serie(com_name)
