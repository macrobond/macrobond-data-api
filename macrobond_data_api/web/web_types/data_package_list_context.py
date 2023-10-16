from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional, Tuple, cast, Iterable, Iterator

import ijson

from macrobond_data_api.common.types._parse_iso8601 import _parse_iso8601

from ..web_types.data_package_list_state import DataPackageListState
from ..web_types.data_package_body import DataPackageBody
from ..session import _raise_on_error
from .._responseAsFileObject import _ResponseAsFileObject

if TYPE_CHECKING:  # pragma: no cover
    from ..web_api import WebApi
    from requests import Response

# work in progress


class DataPackageListContext(ABC):
    @abstractmethod
    def __enter__(self) -> "DataPackageListIterable":
        ...

    @abstractmethod
    def __exit__(self, exception_type: Any, exception_value: Any, traceback: Any) -> None:
        ...


class DataPackageListIterable(ABC, Iterable[Tuple[str, datetime]]):
    @property
    @abstractmethod
    def body(self) -> DataPackageBody:
        """_"""


class _DataPackageListContext(DataPackageListContext, DataPackageListIterable, Iterator[Tuple[str, datetime]]):
    response_: Optional["Response"]
    _ijson_parse: Any
    _body: Optional[DataPackageBody]

    @property
    def body(self) -> DataPackageBody:
        return cast(DataPackageBody, self._body)

    def __init__(self, if_modified_since: Optional[datetime], webApi: "WebApi") -> None:
        self._if_modified_since = if_modified_since
        self._webApi: Optional["WebApi"] = webApi
        self._iterator_started = False

    def __enter__(self) -> "_DataPackageListContext":
        params = {}
        if self._if_modified_since:
            params["ifModifiedSince"] = self._if_modified_since.isoformat()

        if self._webApi is None:
            raise Exception("obj is closed")

        try:
            self.response_ = self._webApi._session.get("v1/series/getdatapackagelist", params=params, stream=True)
            self._webApi = None

            _raise_on_error(self.response_)
            self._ijson_parse = ijson.parse(_ResponseAsFileObject(self.response_))
            self._set_body()

            return self

        except Exception as e:
            self.__exit__(None, None, None)
            raise e

    def __exit__(self, exception_type: Any, exception_value: Any, traceback: Any) -> None:
        self._webApi = None
        if self.response_:
            self.response_.close()
            self.response_ = None

    def _set_body(self) -> None:
        time_stamp_for_if_modified_since: Optional[datetime] = None
        download_full_list_on_or_after: Optional[datetime] = None
        state: Optional[DataPackageListState] = None
        for prefix, event, value in self._ijson_parse:
            if prefix == "timeStampForIfModifiedSince":
                if event != "string":
                    raise Exception("bad format: timeStampForIfModifiedSince is not a string")
                time_stamp_for_if_modified_since = _parse_iso8601(value)
            elif prefix == "downloadFullListOnOrAfter":
                if event != "string":
                    raise Exception("bad format: downloadFullListOnOrAfter is not a string")
                download_full_list_on_or_after = _parse_iso8601(value)
            elif prefix == "state":
                if event != "number":
                    raise Exception("bad format: state is not a number")
                state = DataPackageListState(value)
            elif event == "start_array":
                if prefix != "entities":
                    raise Exception("bad format: event start_array do not have a prefix of entities")
                break

        if state is None:
            raise Exception("bad format: state was not found")
        if time_stamp_for_if_modified_since is None:
            raise Exception("bad format: timeStampForIfModifiedSince was not found")
        if not self._if_modified_since and download_full_list_on_or_after is None:
            raise Exception("bad format: downloadFullListOnOrAfter was not found")

        self._body = DataPackageBody(time_stamp_for_if_modified_since, download_full_list_on_or_after, state)

    def __iter__(self) -> "_DataPackageListContext":
        if self._iterator_started:
            raise Exception("iterator has already started")
        self._iterator_started = True
        return self

    def __next__(self) -> Tuple[str, datetime]:
        name = ""
        modified: Optional[datetime] = None

        while True:
            prefix, event, value = next(self._ijson_parse)
            if event == "end_map":
                if name == "":
                    raise Exception("bad format: name was not found")
                if modified is None:
                    raise Exception("bad format: modified was not found")
                return (name, modified)

            if event == "end_array":
                raise StopIteration()

            if prefix == "entities.item.name":
                if event != "string":
                    raise Exception("bad format: entities.item.name is not a string")
                name = value
            elif prefix == "entities.item.modified":
                if event != "string":
                    raise Exception("bad format: entities.item.modified is not a string")
                modified = _parse_iso8601(value)
