from datetime import datetime, timezone
from io import BytesIO
from json import dumps as json_dumps
from typing import Any, Dict, List, Optional
import pytest

from requests import Response

from macrobond_data_api.web import WebApi
from macrobond_data_api.web.data_package_list_poller import DataPackageListPoller, RetryException
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


def http_500_response() -> Response:
    response = Response()
    response.status_code = 500
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

    def on_full_listing_begin(self, subscription: "DataPackageBody") -> None:
        raise Exception("should not be called")

    def on_full_listing_batch(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
        raise Exception("should not be called")

    def on_full_listing_end(self, is_aborted: bool, exception: Optional[Exception]) -> None:
        raise Exception("should not be called")

    def on_incremental_begin(self, subscription: "DataPackageBody") -> None:
        raise Exception("should not be called")

    def on_incremental_batch(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
        raise Exception("should not be called")

    def on_incremental_end(self, is_aborted: bool, exception: Optional[Exception]) -> None:
        raise Exception("should not be called")


# _run_full_listing
def test_full_listing() -> None:
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
            hit_test(2)
            assert secs == self.on_error_delay

        def on_full_listing_begin(self, subscription: "DataPackageBody") -> None:
            hit_test(3)

        def on_full_listing_batch(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
            hit_test(4)

        def on_full_listing_end(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(5)
            self.abort()

    api = get_api(http_500_response(), get_json_response(DataPackageListState.FULL_LISTING))

    _TestDataPackageListPoller(api, chunk_size=200).start()

    assert hit == 5


def test_full_listing_error() -> None:
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
            hit = hit_test(2, 3, 4) - 1
            assert secs == self.on_retry_delay * hit

    api = get_api(
        http_500_response(),
        http_500_response(),
        http_500_response(),
        http_500_response(),
    )
    with pytest.raises(RetryException, match="Retry Exception"):
        _TestDataPackageListPoller(api, chunk_size=200).start()

    assert hit == 4


# _run_listing
def test_listing() -> None:
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
            hit_test(3)
            assert secs == self.on_error_delay

        def now(self) -> datetime:
            hit_test(2)
            return datetime(2000, 1, 1, tzinfo=timezone.utc)

        def on_incremental_begin(self, subscription: "DataPackageBody") -> None:
            hit_test(4)

        def on_incremental_batch(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
            hit_test(5)

        def on_incremental_end(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(6)
            self.abort()

    api = get_api(http_500_response(), get_json_response(DataPackageListState.UP_TO_DATE))

    _TestDataPackageListPoller(
        api,
        download_full_list_on_or_after=datetime(3000, 1, 1, tzinfo=timezone.utc),
        time_stamp_for_if_modified_since=datetime(1000, 1, 1, tzinfo=timezone.utc),
    ).start()

    assert hit == 6


def test_listing_error() -> None:
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

        def sleep(self, secs: float) -> None:
            hit = hit_test(3, 4, 5) - 2
            assert secs == self.on_retry_delay * hit

    api = get_api(
        http_500_response(),
        http_500_response(),
        http_500_response(),
        http_500_response(),
    )

    with pytest.raises(RetryException, match="Retry Exception"):
        _TestDataPackageListPoller(
            api,
            download_full_list_on_or_after=datetime(3000, 1, 1, tzinfo=timezone.utc),
            time_stamp_for_if_modified_since=datetime(1000, 1, 1, tzinfo=timezone.utc),
        ).start()

    assert hit == 5


# _run_listing and _run_listing_incomplete
def test_listing_and_listing_incomplete() -> None:
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
            hit = hit_test(5, 6, 12)
            if hit == 5:
                assert secs == self.incomplete_delay
            elif hit == 6:
                assert secs == self.on_error_delay
            elif hit == 12:
                assert secs == self.up_to_date_delay
                raise Exception("End of test")

        def now(self) -> datetime:
            hit_test(2)
            return datetime(2000, 1, 1, tzinfo=timezone.utc)

        def on_incremental_begin(self, subscription: "DataPackageBody") -> None:
            hit_test(3)

        def on_incremental_batch(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
            if hit_test(4, 7) == 4:
                assert subscription.state == DataPackageListState.INCOMPLETE
            elif hit == 7:
                assert subscription.state == DataPackageListState.UP_TO_DATE

        def on_incremental_end(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(8)
            self.abort()

    api = get_api(
        get_json_response(DataPackageListState.INCOMPLETE),
        http_500_response(),
        get_json_response(DataPackageListState.UP_TO_DATE),
    )

    _TestDataPackageListPoller(
        api,
        download_full_list_on_or_after=datetime(3000, 1, 1, tzinfo=timezone.utc),
        time_stamp_for_if_modified_since=datetime(1000, 1, 1, tzinfo=timezone.utc),
    ).start()

    assert hit == 8


def test_listing_and_listing_incomplete_error() -> None:
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
            hit = hit_test(5, 6, 7, 8)
            if hit == 5:
                assert secs == self.incomplete_delay
            else:
                assert secs == self.on_retry_delay * (hit - 5)

        def now(self) -> datetime:
            hit_test(2)
            return datetime(2000, 1, 1, tzinfo=timezone.utc)

        def on_incremental_begin(self, subscription: "DataPackageBody") -> None:
            hit_test(3)

        def on_incremental_batch(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
            hit_test(4)
            assert subscription.state == DataPackageListState.INCOMPLETE

        def on_incremental_end(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(9)
            self.abort()
            assert is_aborted is False
            assert exception is not None

    api = get_api(
        get_json_response(DataPackageListState.INCOMPLETE),
        http_500_response(),
        http_500_response(),
        http_500_response(),
        http_500_response(),
    )

    _TestDataPackageListPoller(
        api,
        download_full_list_on_or_after=datetime(3000, 1, 1, tzinfo=timezone.utc),
        time_stamp_for_if_modified_since=datetime(1000, 1, 1, tzinfo=timezone.utc),
    ).start()

    assert hit == 9
