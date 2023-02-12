from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Sequence, overload

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore

__pdoc__ = {
    "SearchResultLong.__init__": False,
}


@dataclass(init=False)
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

    def to_pd_data_frame(self) -> "DataFrame":
        """
        Return the result as a `DataFrame`.
        """
        import pandas  # pylint: disable=import-outside-toplevel

        return pandas.DataFrame(self)

    @overload
    def __getitem__(self, i: int) -> str:
        ...

    @overload
    def __getitem__(self, s: slice) -> List[str]:
        ...

    def __getitem__(self, key):  # type: ignore
        return self.entities[key]

    def __len__(self) -> int:
        return len(self.entities)