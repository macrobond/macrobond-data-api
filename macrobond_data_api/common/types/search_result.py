from dataclasses import dataclass
from typing import Any, Mapping, TYPE_CHECKING, List, Sequence, overload

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame
    from .metadata import Metadata

__pdoc__ = {
    "SearchResult.__init__": False,
}


@dataclass(init=False)
class SearchResult(Sequence["Metadata"]):
    """
    The result of a entity search operation.
    """

    __slots__ = ("entities", "is_truncated")

    entities: Sequence["Metadata"]
    is_truncated: bool

    def __init__(self, entities: List["Metadata"], is_truncated: bool) -> None:
        super().__init__()
        self.entities = entities
        """
        A sequence of the metadata of the entities found.
        """
        self.is_truncated = is_truncated
        """
        Indicates whether the search result was too long and truncated.
        """

    def to_dict(self) -> List[Mapping[str, Any]]:
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

    def _repr_html_(self) -> str:
        return self.to_pd_data_frame()._repr_html_()

    @overload
    def __getitem__(self, i: int) -> "Metadata":
        pass

    @overload
    def __getitem__(self, s: slice) -> Sequence["Metadata"]:
        pass

    def __getitem__(self, key):  # type: ignore
        return self.entities[key]

    def __len__(self) -> int:
        return len(self.entities)
