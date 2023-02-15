from dataclasses import dataclass

from typing import TYPE_CHECKING, Any, Dict, Sequence, overload

from macrobond_data_api.common.types.vintage_series import VintageSeries

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore

__pdoc__ = {
    "GetAllVintageSeriesResult.__init__": False,
}


@dataclass(init=False)
class GetAllVintageSeriesResult(Sequence[VintageSeries]):
    """
    The result of downloading all vintages of a time series.
    """

    __slots__ = ("series", "series_name")

    series: Sequence[VintageSeries]
    series_name: str

    def __init__(self, series: Sequence[VintageSeries], series_name: str) -> None:
        super().__init__()
        self.series = series
        """A sequence of time series corresponding to the vintages."""
        self.series_name = series_name
        """The name of the requested series."""

    def to_pd_data_frame(self) -> "DataFrame":
        """
        Return the result as a Pandas DataFrame.
        """
        import pandas  # pylint: disable=import-outside-toplevel

        data = [x.values_to_pd_series() for x in self]
        data_frame = pandas.concat(data, axis=1, keys=[s.revision_time_stamp for s in self])
        data_frame = data_frame.sort_index()
        return data_frame

    def to_dict(self) -> Dict[str, Any]:
        """
        Return the result as a dictionary.
        """
        return {"series_name": self.series_name, "series": [x.to_dict() for x in self]}

    def _repr_html_(self) -> str:
        return self.to_pd_data_frame()._repr_html_()

    @overload
    def __getitem__(self, i: int) -> VintageSeries:
        ...

    @overload
    def __getitem__(self, s: slice) -> Sequence[VintageSeries]:
        ...

    def __getitem__(self, key):  # type: ignore
        return self.series[key]

    def __len__(self) -> int:
        return len(self.series)
