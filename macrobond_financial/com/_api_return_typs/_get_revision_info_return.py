# -*- coding: utf-8 -*-

from typing import Sequence, Tuple, List, TYPE_CHECKING

from macrobond_financial.common.api_return_typs import (
    GetRevisionInfoReturn,
    RevisionInfo,
)

from macrobond_financial.common.typs import GetEntitiesError

from macrobond_financial.common._get_pandas import _get_pandas


if TYPE_CHECKING:  # pragma: no cover
    from macrobond_financial.common.api_return_typs import RevisionInfoDict
    from ..com_typs import Database, SeriesWithRevisions, Series as ComSeries
    from ..com_api import ComApi
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class _GetRevisionInfoReturn(GetRevisionInfoReturn):
    def __init__(
        self,
        database: "Database",
        series_names: Sequence[str],
        raise_error: bool,
    ) -> None:
        super().__init__()
        self.__database = database
        self.__series_names = series_names
        self.__raise_error = raise_error

    def fetch_series_with_revisions(self) -> Tuple["SeriesWithRevisions", ...]:
        series = self.__database.FetchSeriesWithRevisions(self.__series_names)

        GetEntitiesError.raise_if(
            self.__raise_error,
            map(
                lambda x, y: (x, y.ErrorMessage if y.IsError else None),
                self.__series_names,
                series,
            ),
        )

        return series

    def object(self) -> List[RevisionInfo]:
        def to_obj(name: str, serie: "SeriesWithRevisions"):
            if serie.IsError:
                return RevisionInfo(
                    name,
                    serie.ErrorMessage,
                    False,
                    False,
                    None,
                    None,
                    tuple(),
                )

            vintage_time_stamps = tuple(serie.GetVintageDates())

            time_stamp_of_first_revision = (
                vintage_time_stamps[0] if serie.HasRevisions else None
            )
            time_stamp_of_last_revision = (
                vintage_time_stamps[-1] if serie.HasRevisions else None
            )

            return RevisionInfo(
                name,
                "",
                serie.StoresRevisions,
                serie.HasRevisions,
                time_stamp_of_first_revision,
                time_stamp_of_last_revision,
                vintage_time_stamps,
            )

        return list(
            map(to_obj, self.__series_names, self.fetch_series_with_revisions())
        )

    def dict(self) -> List["RevisionInfoDict"]:
        def to_dict(name: str, serie: "SeriesWithRevisions") -> "RevisionInfoDict":
            if serie.IsError:
                return {
                    "name": name,
                    "error_message": serie.ErrorMessage,
                }

            vintage_time_stamps = tuple(serie.GetVintageDates())

            time_stamp_of_first_revision = (
                vintage_time_stamps[0] if serie.HasRevisions else None
            )
            time_stamp_of_last_revision = (
                vintage_time_stamps[-1] if serie.HasRevisions else None
            )

            return {
                "name": name,
                "has_revisions": serie.HasRevisions,
                "stores_revisions": serie.StoresRevisions,
                "time_stamp_of_first_revision": time_stamp_of_first_revision,
                "time_stamp_of_last_revision": time_stamp_of_last_revision,
                "vintage_time_stamps": vintage_time_stamps,
            }

        return list(
            map(to_dict, self.__series_names, self.fetch_series_with_revisions())
        )

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.dict()
        return pandas.DataFrame(*args, **kwargs)
