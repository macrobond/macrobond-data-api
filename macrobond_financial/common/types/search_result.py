# -*- coding: utf-8 -*-

from typing import Any, Dict, Sequence, Union, Tuple, overload, TYPE_CHECKING

from .._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore


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
        return f"SearchResult of {len(self)} entities, is_truncated: {self.is_truncated}"

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

    def to_dict(self) -> Tuple[Dict[str, Any], ...]:
        return self.entities

    # def to_pd_data_frame(self) -> "DataFrame":
    #     pandas = _get_pandas()
    #     return pandas.DataFrame(self.entities)

    def to_pd_data_frame(self) -> "DataFrame":
        """
        Return the result as a `DataFrame`.
        """
        pandas = _get_pandas()
        return pandas.DataFrame(self.entities)
