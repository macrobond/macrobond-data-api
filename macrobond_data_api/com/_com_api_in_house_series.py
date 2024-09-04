from datetime import datetime
from collections.abc import Sequence as ABC_Sequence
from typing import TYPE_CHECKING, Dict, Optional, Sequence, Union, Any

from macrobond_data_api.com._fix_datetime import _fix_datetime
from macrobond_data_api.common.enums import SeriesWeekdays, SeriesFrequency

if TYPE_CHECKING:  # pragma: no cover
    from .com_api import ComApi


def _set_metadata(metadata: Dict[str, Any], name: str, val: Any) -> None:
    if name in metadata and metadata[name] != val:
        raise ValueError(f"{name} in metadata does not match {name}")


def upload_series(
    self: "ComApi",
    name: str,
    description: str,
    region: str,
    category: str,
    frequency: SeriesFrequency,
    values: Sequence[Optional[float]],
    start_date_or_dates: Union[datetime, Sequence[datetime]],
    day_mask: SeriesWeekdays = SeriesWeekdays.MONDAY_TO_FRIDAY,
    metadata: Optional[Dict[str, Any]] = None,
    forecast_flags: Optional[Sequence[bool]] = None,
) -> None:
    if isinstance(start_date_or_dates, datetime):
        if start_date_or_dates.tzinfo is None:
            raise ValueError("start_date_or_dates must have a timezone")
        start_date_or_dates = _fix_datetime(start_date_or_dates)

    else:
        if not isinstance(start_date_or_dates, list):
            start_date_or_dates = list(start_date_or_dates)

        if any(x.tzinfo is None for x in start_date_or_dates):
            raise ValueError("start_date_or_dates must have a timezone")

        start_date_or_dates = [_fix_datetime(date) for date in start_date_or_dates]

    com_metadata = self.database.CreateEmptyMetadata()
    if metadata is not None:
        _set_metadata(metadata, "PrimName", name)
        _set_metadata(metadata, "Description", description)
        _set_metadata(metadata, "Region", region)
        _set_metadata(metadata, "IHCategory", category)
        _set_metadata(metadata, "Frequency", frequency.name)
        _set_metadata(metadata, "DayMask", day_mask)

        for key, value in metadata.items():
            if isinstance(value, datetime):
                value = _fix_datetime(value)
            elif (
                isinstance(value, ABC_Sequence)
                and not isinstance(value, str)
                and all(isinstance(item, datetime) for item in value)
            ):
                value = [_fix_datetime(item) for item in value]

            com_metadata.AddValue(key, value)

    values = [float(x) if x is not None else x for x in values]

    if forecast_flags:
        if not isinstance(forecast_flags, list):
            forecast_flags = list(forecast_flags)
        series = self.database.CreateSeriesObjectWithForecastFlags(
            name,
            description,
            region,
            category,
            frequency,
            day_mask,
            start_date_or_dates,
            values,
            forecast_flags,
            com_metadata,
        )
    else:
        series = self.database.CreateSeriesObject(
            name,
            description,
            region,
            category,
            frequency,
            day_mask,
            start_date_or_dates,
            values,
            com_metadata,
        )

    self.database.UploadOneOrMoreSeries(series)


def delete_serie(self: "ComApi", series_name: str) -> None:
    self.database.DeleteOneOrMoreSeries(series_name)
