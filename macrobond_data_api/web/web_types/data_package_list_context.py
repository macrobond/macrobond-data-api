from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional, Tuple, Iterable, Iterator

import ijson

from macrobond_data_api.common.types._parse_iso8601 import _parse_iso8601

from .data_package_list_state import DataPackageListState

if TYPE_CHECKING:  # pragma: no cover
    from ..web_api import WebApi
    from requests import Response

__pdoc__ = {
    "DataPackageListContext.__init__": False,
    "DataPackageListContextManager.__init__": False,
}


class _DataPackageListContextIterator(Iterator[Tuple[str, datetime]], Iterable[Tuple[str, datetime]]):
    _is_uesd = False

    def __init__(self, ijson_parse: Any) -> None:
        self._ijson_parse = ijson_parse

    def __iter__(self) -> Iterator[Tuple[str, datetime]]:
        if self._is_uesd:
            raise Exception("iterator is already used")
        self._is_uesd = True
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


class DataPackageListContext:
    @property
    def time_stamp_for_if_modified_since(self) -> datetime:
        """
        A timestamp to pass as the ifModifiedSince parameter
        in the next request to get incremental updates.
        """
        return self._time_stamp_for_if_modified_since

    @property
    def download_full_list_on_or_after(self) -> Optional[datetime]:
        """
        Recommended earliest next time to request a full list
        by omitting timeStampForIfModifiedSince.
        """
        return self._download_full_list_on_or_after

    @property
    def state(self) -> DataPackageListState:
        """
        The state of this list.
        """
        return self._state

    @property
    def items(self) -> Iterable[Tuple[str, datetime]]:
        """An iterable contining tuples with the name and Timestamp when this entity was last modified"""
        return self._items

    def __init__(
        self,
        time_stamp_for_if_modified_since: datetime,
        download_full_list_on_or_after: Optional[datetime],
        state: DataPackageListState,
        items: _DataPackageListContextIterator,
    ) -> None:
        self._time_stamp_for_if_modified_since = time_stamp_for_if_modified_since
        self._download_full_list_on_or_after = download_full_list_on_or_after
        self._state = state
        self._items = items


def _pars_body(
    ijson_parse: Any,
) -> Tuple[Optional[datetime], Optional[datetime], Optional[DataPackageListState]]:
    time_stamp_for_if_modified_since: Optional[datetime] = None
    download_full_list_on_or_after: Optional[datetime] = None
    state: Optional[DataPackageListState] = None
    for prefix, event, value in ijson_parse:
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
    return time_stamp_for_if_modified_since, download_full_list_on_or_after, state


class DataPackageListContextManager:
    _response: Optional["Response"]

    def __init__(self, if_modified_since: Optional[datetime], webApi: "WebApi") -> None:
        self._if_modified_since = if_modified_since
        self._webApi: Optional["WebApi"] = webApi
        self._iterator_started = False

    def __enter__(self) -> DataPackageListContext:
        params = {}
        if self._if_modified_since:
            params["ifModifiedSince"] = self._if_modified_since.isoformat()

        if self._webApi is None:
            raise Exception("obj is closed")

        try:
            session = self._webApi._session
            self._webApi = None
            self._response = session.get_or_raise("v1/series/getdatapackagelist", params=params, stream=True)

            ijson_parse = ijson.parse(session.response_to_file_object(self._response))

            (
                time_stamp_for_if_modified_since,
                download_full_list_on_or_after,
                state,
            ) = _pars_body(ijson_parse)

            if state is None:
                raise Exception("bad format: state was not found")
            if time_stamp_for_if_modified_since is None:
                raise Exception("bad format: timeStampForIfModifiedSince was not found")
            if not self._if_modified_since and download_full_list_on_or_after is None:
                raise Exception("bad format: downloadFullListOnOrAfter was not found")

            return DataPackageListContext(
                time_stamp_for_if_modified_since,
                download_full_list_on_or_after,
                state,
                _DataPackageListContextIterator(ijson_parse),
            )

        except Exception as e:
            self.__exit__(None, None, None)
            raise e

    def __exit__(self, exception_type: Any, exception_value: Any, traceback: Any) -> None:
        self._webApi = None
        if self._response:
            self._response.close()
            self._response = None
