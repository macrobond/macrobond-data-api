# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Any, Dict, List, Optional, cast, TYPE_CHECKING

from datetime import datetime, timezone

from macrobond_financial.common.types import Entity, Series


if TYPE_CHECKING:  # pragma: no cover
    from ..web_types import SeriesResponse, EntityResponse


def _create_entity(response: "EntityResponse", name: str) -> Entity:
    error_text = response.get("errorText")

    if error_text:
        return Entity(name, error_text, None)

    return Entity(name, None, cast(Dict[str, Any], response["metadata"]))


def _create_series(response: "SeriesResponse", name: str) -> Series:
    error_text = response.get("errorText")

    if error_text:
        return Series(name, error_text, None, None, None)

    dates = tuple(
        map(
            lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").replace(
                tzinfo=timezone.utc
            ),
            cast(List[str], response["dates"]),
        )
    )
    values = tuple(
        map(
            lambda x: float(x) if x else None,
            cast(List[Optional[float]], response["values"]),
        )
    )
    # values = cast(Tuple[Optional[float]], response["values"])
    return Series(name, "", cast(Dict[str, Any], response["metadata"]), values, dates)
