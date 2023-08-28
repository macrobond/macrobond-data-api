from datetime import datetime, timezone


import pytest  # type: ignore[attr-defined]
from macrobond_data_api.common import Api
from macrobond_data_api.common.enums import SeriesFrequency


def _try_delete_series(api: Api, *names: str) -> None:
    for name in names:
        try:
            api.delete_serie(name)
        except:  # noqa: E722
            ...


@pytest.mark.usefixtures("lock_test")
@pytest.mark.usefixtures("assert_no_warnings")
@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_upload_series(api: Api) -> None:
    name = "ih:mb:priv:test_name_py_1"
    _try_delete_series(api, name)
    try:
        api.upload_series(
            name,
            "test_description",
            "us",
            "test_category",
            SeriesFrequency.DAILY,
            [1.0, 2.0, 3.0],
            datetime(2020, 1, 1, tzinfo=timezone.utc),
        )
    finally:
        api.delete_serie(name)
