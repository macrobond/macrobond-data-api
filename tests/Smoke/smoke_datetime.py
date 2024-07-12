import pandas as pd
import pytest
from macrobond_data_api.common.enums import SeriesFrequency
from macrobond_data_api.com import ComClient
from datetime import datetime, timezone


@pytest.mark.usefixtures("lock_test")
@pytest.mark.usefixtures("assert_no_warnings")
def test_datetime_converter_upload_series_multi_values() -> None:
    values = [10, 20, 30]
    dates = [
        datetime(2023, 1, 1, tzinfo=timezone.utc),
        datetime(2023, 1, 2, tzinfo=timezone.utc),
        datetime(2023, 1, 3, tzinfo=timezone.utc),
    ]

    # Create a DataFrame
    df = pd.DataFrame({"Date": dates, "Value": values})
    with ComClient() as mb_api:
        mb_api.upload_series(
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
def test_datetime_converter_upload_series_single_value() -> None:
    with ComClient() as mb_api:
        mb_api.upload_series(
            name="ih:mb:priv:dataframe",
            description="uploading from dataframe",
            region="world",
            category="category",
            frequency=SeriesFrequency.DAILY,
            values=[10],
            start_date_or_dates=pd.Timestamp(datetime(2023, 1, 1, tzinfo=timezone.utc)),
        )
