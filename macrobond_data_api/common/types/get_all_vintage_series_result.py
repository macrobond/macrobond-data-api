from dataclasses import dataclass

from typing import TYPE_CHECKING, Any, Dict, Sequence, overload, List

from macrobond_data_api.common.types.vintage_series import VintageSeries

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame

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

    def __init__(self, series: List[VintageSeries], series_name: str) -> None:
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

        df = pandas.DataFrame(
            {
                **{"date": self.series[len(self.series) - 1].dates},
            }
        )

        for x in self.series:
            arg: Any = {
                **{"date": x.dates},
                **{x.revision_time_stamp: pandas.Series(data=x.values, name="Value", dtype="float64")},
            }
            df_to_merge = pandas.DataFrame(arg)
            df = df.merge(df_to_merge, how="left", left_on="date", right_on="date")

        return df

    def to_dict(self) -> Dict[str, Any]:
        """
        Return the result as a dictionary.
        """
        return {"series_name": self.series_name, "series": [x.to_dict() for x in self]}

    def _repr_html_(self) -> str:
        html = self.to_pd_data_frame()._repr_html_()
        return f"<p>{self.series_name}</p>{html}"

    @overload
    def __getitem__(self, i: int) -> VintageSeries:
        pass

    @overload
    def __getitem__(self, s: slice) -> Sequence[VintageSeries]:
        pass

    def __getitem__(self, key):  # type: ignore
        return self.series[key]

    def __len__(self) -> int:
        return len(self.series)
