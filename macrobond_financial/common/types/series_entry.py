# -*- coding: utf-8 -*-

from datetime import datetime

from typing import Optional

from macrobond_financial.common.enums import (
    SeriesMissingValueMethod,
    SeriesToLowerFrequencyMethod,
    SeriesToHigherFrequencyMethod,
    SeriesPartialPeriodsMethod,
)


class SeriesEntry:

    __slots__ = (
        "name",
        "vintage",
        "missing_value_method",
        "to_lowerfrequency_method",
        "to_higherfrequency_method",
        "partial_periods_method",
    )

    def __init__(
        self,
        name: str,
        vintage: Optional[datetime] = None,
        missing_value_method=SeriesMissingValueMethod.NONE,
        to_lowerfrequency_method=SeriesToLowerFrequencyMethod.AUTO,
        to_higherfrequency_method=SeriesToHigherFrequencyMethod.AUTO,
        partial_periods_method=SeriesPartialPeriodsMethod.NONE,
    ) -> None:
        self.name = name
        self.vintage = vintage
        self.missing_value_method = missing_value_method
        self.to_lowerfrequency_method = to_lowerfrequency_method
        self.to_higherfrequency_method = to_higherfrequency_method
        self.partial_periods_method = partial_periods_method
