# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from macrobond_financial.common.typs import Entity, Series

from ._fill_metadata_from_entity import _fill_metadata_from_entity

if TYPE_CHECKING:  # pragma: no cover
    from ..com_typs import (
        Series as ComSeries,
        Entity as ComEntity,
    )

    from macrobond_financial.common.typs import EntityTypedDict, SeriesTypedDict


def _create_entity(com_entity: "ComEntity", name: str) -> Entity:
    if com_entity.IsError:
        return Entity(name, com_entity.ErrorMessage, None)
    return Entity(name, None, _fill_metadata_from_entity(com_entity))


def _create_entity_dicts(com_entity: "ComEntity", name: str) -> "EntityTypedDict":
    if com_entity.IsError:
        return {
            "Name": name,
            "ErrorMessage": com_entity.ErrorMessage,
        }
    return {"Name": name, "MetaData": _fill_metadata_from_entity(com_entity)}


def _create_series(com_series: "ComSeries", name: str) -> Series:
    if com_series.IsError:
        return Series(name, com_series.ErrorMessage, None, None, None)
    return Series(
        name,
        None,
        _fill_metadata_from_entity(com_series),
        com_series.Values,
        com_series.DatesAtStartOfPeriod,
    )


def _create_series_dicts(com_series: "ComSeries", name: str) -> "SeriesTypedDict":
    if com_series.IsError:
        return {
            "Name": name,
            "ErrorMessage": com_series.ErrorMessage,
        }
    return {
        "Name": name,
        "Values": com_series.Values,
        "Dates": com_series.DatesAtStartOfPeriod,
        "MetaData": _fill_metadata_from_entity(com_series),
    }
