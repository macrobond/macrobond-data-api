from typing import Any, MutableMapping, TYPE_CHECKING, List, Sequence, overload

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore


__pdoc__ = {
    "SearchResult.__init__": False,
}


class SearchResult(Sequence[MutableMapping[str, Any]]):
    """
    The result of a entity search operation.
    """

    __slots__ = ("entities", "is_truncated")

    entities: Sequence[MutableMapping[str, Any]]
    is_truncated: bool

    def __init__(self, entities: Sequence[MutableMapping[str, Any]], is_truncated: bool) -> None:
        super().__init__()
        self.entities = entities
        """
        A sequence of the metadata of the entities found.
        """
        self.is_truncated = is_truncated
        """
        Indicates whether the search result was too long and truncated.
        """

    def __repr__(self) -> str:
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
        import pandas  # pylint: disable=import-outside-toplevel

        return pandas.DataFrame(self)

    @overload
    def __getitem__(self, i: int) -> MutableMapping[str, Any]:
        ...

    @overload
    def __getitem__(self, s: slice) -> List[MutableMapping[str, Any]]:
        ...

    def __getitem__(self, key):  # type: ignore
        return self.entities[key]

    def __len__(self) -> int:
        return len(self.entities)