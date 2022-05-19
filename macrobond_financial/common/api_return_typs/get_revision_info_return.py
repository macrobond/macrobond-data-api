# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List, Tuple, TYPE_CHECKING, overload, Optional, cast
from abc import ABC, abstractmethod

from typing_extensions import TypedDict

from .._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class RevisionInfoDict(TypedDict, total=False):
    name: str
    error_message: str
    stores_revisions: bool
    has_revisions: bool
    time_stamp_of_first_revision: Optional[datetime]
    time_stamp_of_last_revision: Optional[datetime]
    vintage_time_stamps: Tuple[datetime, ...]


class RevisionInfo:
    def __init__(
        self,
        name: str,
        error_message: str,
        stores_revisions: bool,
        has_revisions: bool,
        time_stamp_of_first_revision: Optional[datetime],
        time_stamp_of_last_revision: Optional[datetime],
        vintage_time_stamps: Tuple[datetime, ...],
    ) -> None:
        self.name = name
        self.error_message = error_message
        self.stores_revisions = stores_revisions
        self.has_revisions = has_revisions
        self.time_stamp_of_first_revision = time_stamp_of_first_revision
        self.time_stamp_of_last_revision = time_stamp_of_last_revision
        self.vintage_time_stamps = vintage_time_stamps

    def to_dict(self) -> RevisionInfoDict:
        return cast(RevisionInfoDict, vars(self))

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
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.to_dict()
        return pandas.DataFrame(*args, **kwargs)


class GetRevisionInfoReturn(ABC):
    @abstractmethod
    def object(self) -> List[RevisionInfo]:
        ...  # pragma: no cover

    def dict(self) -> List[RevisionInfoDict]:
        return list(map(lambda x: x.to_dict(), self.object()))

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
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.dict()
        return pandas.DataFrame(*args, **kwargs)
