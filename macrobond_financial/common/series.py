# -*- coding: utf-8 -*-

from typing import Any, Dict, Tuple, Optional, List, cast, TYPE_CHECKING

from datetime import datetime

from .entity import Entity

if TYPE_CHECKING:  # pragma: no cover

    from .entity import EntityColumnsLiterals, EntityTypedDict

    from typing_extensions import Literal

    SeriesColumnsLiterals = Literal[EntityColumnsLiterals, "Values", "Dates"]

    SeriesColumns = List[SeriesColumnsLiterals]

    class SeriesTypedDict(EntityTypedDict, total=False):
        Values: Tuple[Optional[float], ...]
        Dates: Tuple[datetime, ...]


class Series(Entity):
    """Interface for a Macrobond time series."""

    def __init__(
        self,
        name: str,
        error_message: Optional[str],
        metadata: Optional[Dict[str, Any]],
        values: Optional[Tuple[Optional[float], ...]],
        dates: Optional[Tuple[datetime, ...]],
    ) -> None:
        super().__init__(name, error_message, metadata)
        if values is None:
            self.values: Tuple[Optional[float], ...] = tuple()
            self.dates: Tuple[datetime, ...] = tuple()
        else:
            self.values = values
            self.dates = cast(Tuple[datetime, ...], dates)
