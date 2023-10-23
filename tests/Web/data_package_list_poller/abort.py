from datetime import datetime, timezone
from io import BytesIO
from json import dumps as json_dumps
from typing import Any, Dict, List, Optional

from requests import Response

from macrobond_data_api.web import WebApi
from macrobond_data_api.web.data_package_list_poller import DataPackageListPoller
from macrobond_data_api.web.session import Session
from macrobond_data_api.web.web_types import DataPackageBody, DataPackageListItem, DataPackageListState


class TestAuth2Session:
    __test__ = False

    def __init__(self, *responses: Response):
        self.index = 0
        self.responses = responses

    def request(self, *args: Any, **kwargs: Any) -> Response:  # pylint: disable=unused-argument
        response = self.responses[self.index]
        self.index += 1
        return response


def get_api(*responses: Response) -> WebApi:
    return WebApi(Session("", "", test_auth2_session=TestAuth2Session(*responses)))


def get_json_response(
    state: DataPackageListState,
    downloadFullListOnOrAfter: str = "2000-02-01T04:05:06",
    timeStampForIfModifiedSince: str = "2000-02-02T04:05:06",
    entities: Optional[List[Dict[str, str]]] = None,
) -> Response:
    if entities is None:
        entities = [
            {"name": "sek", "modified": "2000-02-03T04:05:06"},
            {"name": "dkk", "modified": "2000-02-04T04:05:06"},
            {"name": "usgdp", "modified": "2000-02-05T04:05:06"},
        ]
    json = json_dumps(
        {
            "downloadFullListOnOrAfter": downloadFullListOnOrAfter,
            "timeStampForIfModifiedSince": timeStampForIfModifiedSince,
            "state": state,
            "entities": entities,
        }
    )
    response = Response()
    response.status_code = 200
    response.raw = BytesIO(bytes(json, "utf-8"))
    return response


class TestDataPackageListPoller(DataPackageListPoller):
    __test__ = False

    def __init__(
        self,
        api: WebApi,
        download_full_list_on_or_after: Optional[datetime] = None,
        time_stamp_for_if_modified_since: Optional[datetime] = None,
        chunk_size: int = 200,
    ):
        super().__init__(api, download_full_list_on_or_after, time_stamp_for_if_modified_since, chunk_size)
        self._sleep = self.sleep
        self._now = self.now

    def sleep(self, secs: float) -> None:
        raise Exception("should not be called")

    def now(self) -> datetime:
        raise Exception("should not be called")

    def on_full_listing_start(self, subscription: "DataPackageBody") -> None:
        raise Exception("should not be called")

    def on_full_listing_items(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
        raise Exception("should not be called")

    def on_full_listing_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
        raise Exception("should not be called")

    def on_incremental_start(self, subscription: "DataPackageBody") -> None:
        raise Exception("should not be called")

    def on_incremental_items(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
        raise Exception("should not be called")

    def on_incremental_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
        raise Exception("should not be called")


def test_abort_full_listing_1() -> None:
    hit = 0

    def hit_test(*now: int) -> int:
        nonlocal hit
        hit += 1
        assert hit in now
        return hit

    class _TestDataPackageListPoller(TestDataPackageListPoller):
        __test__ = False

        def _test_access(self) -> None:
            hit_test(1)

        def on_full_listing_start(self, subscription: "DataPackageBody") -> None:
            hit_test(2)
            self.abort()

        def on_full_listing_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(3)
            assert is_aborted is True
            assert exception is None

    api = get_api(get_json_response(DataPackageListState.FULL_LISTING))

    _TestDataPackageListPoller(api, chunk_size=1).start()

    assert hit == 3


def test_abort_full_listing_2() -> None:
    hit = 0

    def hit_test(*now: int) -> int:
        nonlocal hit
        hit += 1
        assert hit in now
        return hit

    class _TestDataPackageListPoller(TestDataPackageListPoller):
        __test__ = False

        def _test_access(self) -> None:
            hit_test(1)

        def on_full_listing_start(self, subscription: "DataPackageBody") -> None:
            hit_test(2)

        def on_full_listing_items(self, subscription: DataPackageBody, items: List[DataPackageListItem]) -> None:
            if hit_test(3, 4) == 4:
                self.abort()

        def on_full_listing_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(5)
            assert is_aborted is True
            assert exception is None

    api = get_api(get_json_response(DataPackageListState.FULL_LISTING))

    _TestDataPackageListPoller(api, chunk_size=1).start()

    assert hit == 5


def test_abort_full_listing_3() -> None:
    hit = 0

    def hit_test(*now: int) -> int:
        nonlocal hit
        hit += 1
        assert hit in now
        return hit

    class _TestDataPackageListPoller(TestDataPackageListPoller):
        __test__ = False

        def _test_access(self) -> None:
            hit_test(1)

        def on_full_listing_start(self, subscription: "DataPackageBody") -> None:
            hit_test(2)

        def on_full_listing_items(self, subscription: DataPackageBody, items: List[DataPackageListItem]) -> None:
            hit_test(3)

        def on_full_listing_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(4)
            assert is_aborted is False
            assert exception is None
            self.abort()

    api = get_api(get_json_response(DataPackageListState.FULL_LISTING))

    _TestDataPackageListPoller(api).start()

    assert hit == 4


# test_abort_listing


def test_abort_listing_1() -> None:
    hit = 0

    def hit_test(*now: int) -> int:
        nonlocal hit
        hit += 1
        assert hit in now
        return hit

    class _TestDataPackageListPoller(TestDataPackageListPoller):
        __test__ = False

        def _test_access(self) -> None:
            hit_test(1)

        def now(self) -> datetime:
            hit_test(2)
            return datetime(2000, 1, 1, tzinfo=timezone.utc)

        def on_incremental_start(self, subscription: "DataPackageBody") -> None:
            hit_test(3)
            self.abort()

        def on_incremental_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(4)
            assert is_aborted is True
            assert exception is None

    api = get_api(get_json_response(DataPackageListState.UP_TO_DATE))

    _TestDataPackageListPoller(
        api,
        download_full_list_on_or_after=datetime(3000, 1, 1, tzinfo=timezone.utc),
        time_stamp_for_if_modified_since=datetime(1000, 1, 1, tzinfo=timezone.utc),
    ).start()

    assert hit == 4


def test_abort_listing_2() -> None:
    hit = 0

    def hit_test(*now: int) -> int:
        nonlocal hit
        hit += 1
        assert hit in now
        return hit

    class _TestDataPackageListPoller(TestDataPackageListPoller):
        __test__ = False

        def _test_access(self) -> None:
            hit_test(1)

        def now(self) -> datetime:
            hit_test(2)
            return datetime(2000, 1, 1, tzinfo=timezone.utc)

        def on_incremental_start(self, subscription: "DataPackageBody") -> None:
            hit_test(3)

        def on_incremental_items(self, subscription: DataPackageBody, items: List[DataPackageListItem]) -> None:
            if hit_test(4):
                self.abort()

        def on_incremental_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(5)
            assert is_aborted is True
            assert exception is None

    api = get_api(get_json_response(DataPackageListState.UP_TO_DATE))

    _TestDataPackageListPoller(
        api,
        download_full_list_on_or_after=datetime(3000, 1, 1, tzinfo=timezone.utc),
        time_stamp_for_if_modified_since=datetime(1000, 1, 1, tzinfo=timezone.utc),
        chunk_size=1,
    ).start()

    assert hit == 5


def test_abort_listing_3() -> None:
    hit = 0

    def hit_test(*now: int) -> int:
        nonlocal hit
        hit += 1
        assert hit in now
        return hit

    class _TestDataPackageListPoller(TestDataPackageListPoller):
        __test__ = False

        def _test_access(self) -> None:
            hit_test(1)

        def now(self) -> datetime:
            hit_test(2)
            return datetime(2000, 1, 1, tzinfo=timezone.utc)

        def on_incremental_start(self, subscription: "DataPackageBody") -> None:
            hit_test(3)

        def on_incremental_items(self, subscription: DataPackageBody, items: List[DataPackageListItem]) -> None:
            hit_test(4)

        def on_incremental_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(5)
            assert is_aborted is False
            assert exception is None
            self.abort()

    api = get_api(get_json_response(DataPackageListState.UP_TO_DATE))

    _TestDataPackageListPoller(
        api,
        download_full_list_on_or_after=datetime(3000, 1, 1, tzinfo=timezone.utc),
        time_stamp_for_if_modified_since=datetime(1000, 1, 1, tzinfo=timezone.utc),
    ).start()

    assert hit == 5


# test_abort_listing_and_listing_incomplete


def test_abort_listing_and_listing_incomplete_1() -> None:
    hit = 0

    def hit_test(*now: int) -> int:
        nonlocal hit
        hit += 1
        assert hit in now
        return hit

    class _TestDataPackageListPoller(TestDataPackageListPoller):
        __test__ = False

        def _test_access(self) -> None:
            hit_test(1)

        def sleep(self, secs: float) -> None:
            hit_test(5)

        def now(self) -> datetime:
            hit_test(2)
            return datetime(2000, 1, 1, tzinfo=timezone.utc)

        def on_incremental_start(self, subscription: "DataPackageBody") -> None:
            hit_test(3)

        def on_incremental_items(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
            if hit_test(4, 6) == 6:
                self.abort()

        def on_incremental_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(7)
            assert is_aborted is True
            assert exception is None

    api = get_api(
        get_json_response(DataPackageListState.INCOMPLETE), get_json_response(DataPackageListState.UP_TO_DATE)
    )

    _TestDataPackageListPoller(
        api,
        download_full_list_on_or_after=datetime(3000, 1, 1, tzinfo=timezone.utc),
        time_stamp_for_if_modified_since=datetime(1000, 1, 1, tzinfo=timezone.utc),
    ).start()

    assert hit == 7


def test_abort_listing_and_listing_incomplete_2() -> None:
    hit = 0

    def hit_test(*now: int) -> int:
        nonlocal hit
        hit += 1
        assert hit in now
        return hit

    class _TestDataPackageListPoller(TestDataPackageListPoller):
        __test__ = False

        def _test_access(self) -> None:
            hit_test(1)

        def sleep(self, secs: float) -> None:
            hit_test(5)

        def now(self) -> datetime:
            hit_test(2)
            return datetime(2000, 1, 1, tzinfo=timezone.utc)

        def on_incremental_start(self, subscription: "DataPackageBody") -> None:
            hit_test(3)

        def on_incremental_items(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
            hit_test(4, 6)

        def on_incremental_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(7)
            assert is_aborted is False
            assert exception is None
            self.abort()

    api = get_api(
        get_json_response(DataPackageListState.INCOMPLETE), get_json_response(DataPackageListState.UP_TO_DATE)
    )

    _TestDataPackageListPoller(
        api,
        download_full_list_on_or_after=datetime(3000, 1, 1, tzinfo=timezone.utc),
        time_stamp_for_if_modified_since=datetime(1000, 1, 1, tzinfo=timezone.utc),
    ).start()

    assert hit == 7
