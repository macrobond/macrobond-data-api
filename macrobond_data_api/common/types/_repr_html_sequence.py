from typing import Generic, Sequence, TypeVar, overload


_TypeVar = TypeVar("_TypeVar")


class _ReprHtmlSequence(Sequence[_TypeVar], Generic[_TypeVar]):
    __slots__ = ("items",)

    items: Sequence[_TypeVar]

    def __init__(self, items: Sequence[_TypeVar]) -> None:
        super().__init__()
        self.items = items

    @overload
    def __getitem__(self, i: int) -> _TypeVar:
        ...

    @overload
    def __getitem__(self, s: slice) -> Sequence[_TypeVar]:
        ...

    def __getitem__(self, key):  # type: ignore
        return self.items[key]

    def __len__(self) -> int:
        return len(self.items)

    def _repr_html_(self) -> str:
        return "".join(x._repr_html_() for x in self)  # type: ignore
