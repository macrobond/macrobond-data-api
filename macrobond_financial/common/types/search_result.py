# -*- coding: utf-8 -*-

from typing import Any, Dict, Sequence, Union, Tuple, overload, TYPE_CHECKING

from .._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


# TODO: @mb-jp in inheritance dict [str, Any] ?


class SearchResult(Sequence[Dict[str, Any]]):
    """
    The result of a entity search operation.
    """

    def __init__(self, entities: Tuple[Dict[str, Any], ...], is_truncated: bool) -> None:
        self.entities = entities
        """
        A sequence of the metadata of the entities found.
        """
        self.is_truncated = is_truncated
        """
        Indicates whether the search result was too long and truncated.
        """

    def __str__(self):
        return f"SearchResult of {len(self)} entities, is is_truncated {self.is_truncated}"

    def __repr__(self):
        return str(self)

    @overload
    def __getitem__(self, idx: int) -> Dict[str, Any]:
        ...

    @overload
    def __getitem__(self, _slice: slice) -> Sequence[Dict[str, Any]]:
        ...

    def __getitem__(self, idx_or_slice: Union[int, slice]):
        return self.entities.__getitem__(idx_or_slice)

    def __len__(self) -> int:
        return len(self.entities)

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: "pandas_typing.Axes" = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        """
        Return the result as a `DataFrame`.
        """
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.entities
        return pandas.DataFrame(*args, **kwargs)
