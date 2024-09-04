from datetime import datetime, timezone

import pytest
import pandas as pd

from macrobond_data_api.common import Api
from macrobond_data_api.common.enums import SeriesFrequency


def _try_delete_series(api: Api, *names: str) -> None:
    for name in names:
        try:
            api.delete_serie(name)
        except Exception:  # pylint: disable=broad-exception-caught
            pass


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


@pytest.mark.usefixtures("lock_test")
@pytest.mark.usefixtures("assert_no_warnings")
@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_datetime_converter_upload_series_multi_values(api: Api) -> None:
    values = [10, 20, 30]
    dates = [
        datetime(2023, 1, 1, tzinfo=timezone.utc),
        datetime(2023, 1, 2, tzinfo=timezone.utc),
        datetime(2023, 1, 3, tzinfo=timezone.utc),
    ]

    # Create a DataFrame
    df = pd.DataFrame({"Date": dates, "Value": values})
    api.upload_series(
        name="ih:mb:priv:dataframe",
        description="uploading from dataframe",
        region="world",
        category="category",
        frequency=SeriesFrequency.DAILY,
        values=df["Value"],
        start_date_or_dates=df["Date"],
    )


@pytest.mark.usefixtures("lock_test")
@pytest.mark.usefixtures("assert_no_warnings")
@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_datetime_converter_upload_series_single_value(api: Api) -> None:
    api.upload_series(
        name="ih:mb:priv:dataframe",
        description="uploading from dataframe",
        region="world",
        category="category",
        frequency=SeriesFrequency.DAILY,
        values=[10],
        start_date_or_dates=pd.Timestamp(datetime(2023, 1, 1, tzinfo=timezone.utc)),
    )
