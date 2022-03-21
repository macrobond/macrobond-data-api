# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Any, Dict, Tuple, List, Optional, cast, TYPE_CHECKING

from datetime import datetime, timezone

from macrobond_financial.common.typs import Entity, Series


if TYPE_CHECKING:  # pragma: no cover
    from macrobond_financial.common.typs import SeriesTypedDict, EntityTypedDict

    from ..web_typs import SeriesResponse, EntityResponse


def _create_entity(response: "EntityResponse", name: str) -> Entity:
    error_text = response.get("errorText")

    if error_text:
        return Entity(name, error_text, None)

    return Entity(name, None, cast(Dict[str, Any], response["metadata"]))


def _add_metadata(
    source: Dict[str, Any], destination: Dict[str, Any] = None
) -> Dict[str, Any]:
    if not destination:
        destination = {}

    for key in source.keys():
        destination["metadata." + key] = source[key]

    return destination


def _create_entity_dicts(response: "EntityResponse", name: str) -> "EntityTypedDict":
    error_text = response.get("errorText")

    if error_text:
        error_entity: "EntityTypedDict" = {
            "Name": name,
            "ErrorMessage": error_text,
        }
        return error_entity

    return _add_metadata(response["metadata"], {"Name": name})  # type: ignore


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

    values = cast(Tuple[Optional[float]], response["values"])
    return Series(name, "", cast(Dict[str, Any], response["metadata"]), values, dates)


def _create_series_dicts(response: "SeriesResponse", name: str) -> "SeriesTypedDict":
    error_text = response.get("errorText")

    if error_text:
        error_series: "SeriesTypedDict" = {
            "Name": name,
            "ErrorMessage": error_text,
        }
        return error_series

    dates = tuple(
        map(
            lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").replace(
                tzinfo=timezone.utc
            ),
            cast(List[str], response["dates"]),
        )
    )

    values = cast(Tuple[Optional[float]], response["values"])

    series: "SeriesTypedDict" = {  # type: ignore
        "Name": name,
        "Values": values,
        "Dates": dates,
    }

    return _add_metadata(response["metadata"], series)  # type: ignore
