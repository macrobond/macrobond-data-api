from typing import TYPE_CHECKING, List, Sequence

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore

__pdoc__ = {
    "SearchResultLong.__init__": False,
}


class SearchResultLong(Sequence[str]):
    """
    The result of a entity search operation.
    """

    __slots__ = ("entities", "is_truncated")

    entities: Sequence[str]
    is_truncated: bool

    def __init__(self, entities: Sequence[str], is_truncated: bool) -> None:
        super().__init__()
        self.entities = entities
        self.is_truncated = is_truncated
        """
        Indicates whether the search result was too long and truncated.
        """

    @property
    def names(self) -> List[str]:
        """
        A sequence of the name of the entities found.
        """
        return list(self)

    def __repr__(self) -> str:
        return f"SearchResultLong of {len(self)} entities, is_truncated: {self.is_truncated}"

    def to_pd_data_frame(self) -> "DataFrame":
        """
        Return the result as a `DataFrame`.
        """
        import pandas  # pylint: disable=import-outside-toplevel

        return pandas.DataFrame(self)

    def __getitem__(self, key):
        return self.entities[key]

    def __len__(self) -> int:
        return len(self.entities)
