# -*- coding: utf-8 -*-

from typing import Sequence, Tuple, List, TYPE_CHECKING

from macrobond_financial.common.api_return_types import (
    GetRevisionInfoReturn,
    RevisionInfo,
)

from macrobond_financial.common.types import GetEntitiesError


if TYPE_CHECKING:  # pragma: no cover
    from ..com_types import Database, SeriesWithRevisions


class _GetRevisionInfoReturn(GetRevisionInfoReturn):
    def __init__(
        self,
        database: "Database",
        series_names: Sequence[str],
        _raise: bool,
    ) -> None:
        super().__init__()
        self._database = database
        self._series_names = series_names
        self._raise = _raise

    def fetch_series_with_revisions(self) -> Tuple["SeriesWithRevisions", ...]:
        series = self._database.FetchSeriesWithRevisions(self._series_names)

        GetEntitiesError.raise_if(
            self._raise,
            map(
                lambda x, y: (x, y.ErrorMessage if y.IsError else None),
                self._series_names,
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

        return list(map(to_obj, self._series_names, self.fetch_series_with_revisions()))
