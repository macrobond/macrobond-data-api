# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import TYPE_CHECKING

from macrobond_financial.common.typs import Entity, GetEntitiesError

from macrobond_financial.common.api_return_typs import GetOneEntityReturn

from macrobond_financial.common._get_pandas import _get_pandas

from ._series_helps import _create_entity, _create_entity_dicts

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session
    from pandas import DataFrame  # type: ignore

    from macrobond_financial.common.typs import EntityTypedDict

    from ..web_typs import EntityResponse


class _GetOneEntityReturn(GetOneEntityReturn):
    def __init__(self, session: "Session", entity_name: str, _raise: bool) -> None:
        self._session = session
        self._entity_name = entity_name
        self._raise = _raise

    def fetch_entities(self) -> "EntityResponse":
        response = self._session.series.fetch_entities(self._entity_name)[0]
        GetEntitiesError.raise_if(
            self._raise, self._entity_name, response.get("errorText")
        )
        return response

    def object(self) -> Entity:
        return _create_entity(self.fetch_entities(), self._entity_name)

    def dict(self) -> "EntityTypedDict":
        return _create_entity_dicts(self.fetch_entities(), self._entity_name)

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = [self.dict()]
        return pandas.DataFrame(*args, **kwargs)

    def metadata_as_data_frame(self) -> "DataFrame":
        pandas = _get_pandas()

        entitie = self.fetch_entities()

        error_text = entitie.get("errorText")
        if error_text:
            return pandas.DataFrame.from_dict(
                {
                    "Name": self._entity_name[0],
                    "ErrorMessage": error_text,
                },
                orient="index",
                columns=["Attributes"],
            )

        metadata = entitie["metadata"]

        return pandas.DataFrame.from_dict(
            metadata, orient="index", columns=["Attributes"]
        )
