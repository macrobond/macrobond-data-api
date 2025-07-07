from typing import Any, Sequence
from datetime import datetime, timezone, timedelta

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
    web_name = "ih:mb:priv:test_name_py_web_1"
    com_name = "ih:mb:priv:test_name_py_com_1"

    _try_delete_series(web, web_name, com_name)

    def upload_and_get_series(api: Api, name: str) -> Series:
        api.upload_series(
            name,
            "test_description_test_1",
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
    web_name = "ih:mb:priv:test_name_py_web_2"
    com_name = "ih:mb:priv:test_name_py_com_2"

    _try_delete_series(web, web_name, com_name)

    def upload_and_get_series(api: Api, name: str) -> Series:
        api.upload_series(
            name,
            "test_description_test_2",
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


@pytest.mark.usefixtures("lock_test")
def test_3(web: WebApi, com: ComApi, test_metadata: Any) -> None:
    web_name = "ih:mb:priv:test_name_py_web_3"
    com_name = "ih:mb:priv:test_name_py_com_3"

    _try_delete_series(web, web_name, com_name)

    def upload_and_get_series(api: Api, name: str) -> Series:
        api.upload_series(
            name,
            "test_description_test_3",
            "us",
            "test_category",
            SeriesFrequency.DAILY,
            [0],
            datetime(2020, 1, 1, tzinfo=timezone.utc),
            # metadata={"RevisionHistorySourceCutOffDate": datetime(2021, 1, 1, tzinfo=timezone.utc)},
            forecast_flags=[True],
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


@pytest.mark.usefixtures("lock_test")
def test_4(web: WebApi, com: ComApi, test_metadata: Any) -> None:
    web_name = "ih:mb:priv:test_name_py_web_4"
    com_name = "ih:mb:priv:test_name_py_com_4"

    _try_delete_series(web, web_name, com_name)

    def upload_and_get_series(api: Api, name: str) -> Series:
        api.upload_series(
            name,
            "test_description_test_4",
            "us",
            "test_category",
            SeriesFrequency.DAILY,
            [-1, -2, -3, 0],
            datetime(2020, 1, 1, tzinfo=timezone.utc),
            # metadata={"RevisionHistorySourceCutOffDate": datetime(2021, 1, 1, tzinfo=timezone.utc)},
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


def _test_5_and_6_impl(api: Api, test_metadata: Any, test_id: str) -> None:

    file_name_1 = "ih:mb:priv:test_name_py_" + test_id + "_1"
    file_name_2 = "ih:mb:priv:test_name_py_" + test_id + "_2"

    _try_delete_series(api, file_name_1, file_name_2)

    def upload_and_get_series(name: str, dates: Sequence[datetime]) -> Series:

        api.upload_series(
            name,
            "test_description_test_" + test_id,
            "us",
            "test_category",
            SeriesFrequency.DAILY,
            [
                -1,
                -2,
            ],
            dates,
        )

        return api.get_one_series(name)

    local_time_zone = datetime.now().astimezone().tzinfo
    if local_time_zone is None:
        raise ValueError("cat not determine local timezone")

    try:
        series1 = upload_and_get_series(
            file_name_1,
            [
                datetime(2020, 1, 1, tzinfo=local_time_zone),
                datetime(2020, 1, 2),
            ],
        )
        series2 = upload_and_get_series(
            file_name_2,
            [
                datetime(2020, 1, 1, tzinfo=local_time_zone),
                datetime(2020, 1, 2, tzinfo=local_time_zone),
            ],
        )

        test_metadata(series1, series2, ignore_keys=["LastModifiedTimeStamp", "PrimName", "Name"])

        series1.name = "test"
        series2.name = "test"

        assert series1.dates[0].year == 2019
        assert series1 == series2
    finally:
        _try_delete_series(api, file_name_1, file_name_2)


@pytest.mark.usefixtures("lock_test")
def test_5(web: WebApi, test_metadata: Any) -> None:
    _test_5_and_6_impl(web, test_metadata, "5")


@pytest.mark.usefixtures("lock_test")
def test_6(com: ComApi, test_metadata: Any) -> None:
    _test_5_and_6_impl(com, test_metadata, "6")
