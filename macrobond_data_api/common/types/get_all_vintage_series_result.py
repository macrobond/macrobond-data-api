# get_all_vintage_series_result


from typing import TYPE_CHECKING, Any, Dict, Sequence, List

from macrobond_data_api.common.types.series import Series

from .._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore


class GetAllVintageSeriesResult(List[Series]):
    """
    The result of downloading all vintages of a time series.
    """

    __slots__ = ("series_name",)

    series_name: str

    def __init__(
        self,
        series: Sequence[Series],
        series_name: str,
    ) -> None:
        super().__init__(series)
        self.series_name = series_name
        """The name of the requested series."""

    @property
    def series(self) -> List[Series]:
        """
        A sequence of time series corresponding to the vintages.
        """
        return list(self)

    def to_pd_data_frame(self) -> "DataFrame":
        """
        Return the result as a Pandas DataFrame.
        """
        pandas = _get_pandas()
        data = list(map(lambda s: s.values_to_pd_series(), self))
        data_frame = pandas.concat(data, axis=1, keys=[s.name for s in self])
        data_frame = data_frame.sort_index()
        return data_frame

    def to_dict(self) -> Dict[str, Any]:
        """
        Return the result as a dictionary.
        """
        return {
            "series_name": self.series_name,
            "series": tuple(map(lambda x: x.to_dict(), self)),
        }

    def __repr__(self):
        return "GetAllVintageSeriesResult series_name: " + self.series_name
