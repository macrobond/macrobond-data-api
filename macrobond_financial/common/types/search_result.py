# -*- coding: utf-8 -*-

from typing import Any, MutableMapping, TYPE_CHECKING, List, Sequence

from .._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore


class SearchResult(List[MutableMapping[str, Any]]):
    """
    The result of a entity search operation.
    """

    __slots__ = ("is_truncated",)

    is_truncated: bool

    def __init__(self, entities: Sequence[MutableMapping[str, Any]], is_truncated: bool) -> None:
        super().__init__(entities)
        self.is_truncated = is_truncated
        """
        Indicates whether the search result was too long and truncated.
        """

    @property
    def entities(self) -> List[MutableMapping[str, Any]]:
        """
        A sequence of the metadata of the entities found.
        """
        return list(self)

    def __repr__(self):
        return f"SearchResult of {len(self)} entities, is_truncated: {self.is_truncated}"

    def to_dict(self) -> List[MutableMapping[str, Any]]:
        """
        Return the result as a dictionary.
        """
        return list(self)

    def to_pd_data_frame(self) -> "DataFrame":
        """
        Return the result as a `DataFrame`.
        """
        pandas = _get_pandas()
        return pandas.DataFrame(self)
