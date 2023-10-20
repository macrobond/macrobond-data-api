from datetime import datetime, timezone
from io import BytesIO
from json import dumps as json_dumps
from typing import Any, Dict, List, Optional

import pytest

from requests import Response

from macrobond_data_api.web import WebApi
from macrobond_data_api.web.data_package_list_poller import DataPackageListPoller
from macrobond_data_api.web.session import Session
from macrobond_data_api.web.web_types import DataPackageBody, DataPackageListItem, DataPackageListState


class TestAuth2Session:
    __test__ = False

    def __init__(self, content: List[bytes]):
        self.index = 0
        self.content = content

    def request(self, *args: Any, **kwargs: Any) -> Response:  # pylint: disable=unused-argument
        response = Response()
        response.status_code = 200
        response.raw = BytesIO(self.content[self.index])
        self.index += 1
        return response


def get_json(
    state: DataPackageListState,
    downloadFullListOnOrAfter: str = "2000-02-01T04:05:06",
    timeStampForIfModifiedSince: str = "2000-02-02T04:05:06",
    entities: Optional[List[Dict[str, str]]] = None,
) -> str:
    if entities is None:
        entities = [
            {"name": "sek", "modified": "2000-02-03T04:05:06"},
            {"name": "dkk", "modified": "2000-02-04T04:05:06"},
            {"name": "usgdp", "modified": "2000-02-05T04:05:06"},
        ]
    return json_dumps(
        {
            "downloadFullListOnOrAfter": downloadFullListOnOrAfter,
            "timeStampForIfModifiedSince": timeStampForIfModifiedSince,
            "state": state,
            "entities": entities,
        }
    )


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


def test_access() -> None:
    hit = 0

    def hit_test(now: int) -> None:
        nonlocal hit
        hit += 1
        assert hit == now

    class _TestAuth2Session:
        __test__ = False

        def request(self, *args: Any, **kwargs: Any) -> Response:  # pylint: disable=unused-argument
            hit_test(1)
            response = Response()
            response.status_code = 403
            return response

    class _TestDataPackageListPoller(TestDataPackageListPoller):
        __test__ = False

    api = WebApi(Session("", "", test_auth2_session=_TestAuth2Session()))
    with pytest.raises(Exception, match="Needs access - The account is not set up to use DataPackageList"):
        _TestDataPackageListPoller(api).start()

    assert hit == 1


# _run_full_listing
def test_full_listing() -> None:
    hit = 0

    def hit_test(now: int) -> None:
        nonlocal hit
        hit += 1
        assert hit == now

    class _TestDataPackageListPoller(TestDataPackageListPoller):
        __test__ = False

        def _test_access(self) -> None:
            hit_test(1)

        def sleep(self, secs: float) -> None:
            hit_test(7)
            assert secs == self.up_to_date_delay
            raise Exception("End of test")

        def on_full_listing_start(self, subscription: "DataPackageBody") -> None:
            hit_test(2)
            assert subscription.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
            assert subscription.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
            assert subscription.state == DataPackageListState.FULL_LISTING

        def on_full_listing_items(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
            nonlocal hit
            hit += 1
            assert subscription.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
            assert subscription.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
            assert subscription.state == DataPackageListState.FULL_LISTING
            if hit == 3:
                assert items == [DataPackageListItem("sek", datetime(2000, 2, 3, 4, 5, 6))]
            if hit == 4:
                assert items == [DataPackageListItem("dkk", datetime(2000, 2, 4, 4, 5, 6))]
            if hit == 5:
                assert items == [DataPackageListItem("usgdp", datetime(2000, 2, 5, 4, 5, 6))]

        def on_full_listing_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(6)
            assert is_aborted is False
            assert exception is None

    json = get_json(DataPackageListState.FULL_LISTING)

    api = WebApi(Session("", "", test_auth2_session=TestAuth2Session([bytes(json, "utf-8")])))

    with pytest.raises(Exception, match="End of test"):
        _TestDataPackageListPoller(api, chunk_size=1).start()

    assert hit == 7


# _run_listing
def test_listing() -> None:
    hit = 0

    def hit_test(now: int) -> None:
        nonlocal hit
        hit += 1
        assert hit == now

    class _TestDataPackageListPoller(TestDataPackageListPoller):
        __test__ = False

        def _test_access(self) -> None:
            hit_test(1)

        def sleep(self, secs: float) -> None:
            hit_test(8)
            assert secs == self.up_to_date_delay
            raise Exception("End of test")

        def now(self) -> datetime:
            hit_test(2)
            return datetime(2000, 1, 1, tzinfo=timezone.utc)

        def on_incremental_start(self, subscription: "DataPackageBody") -> None:
            hit_test(3)
            assert subscription.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
            assert subscription.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
            assert subscription.state == DataPackageListState.UP_TO_DATE

        def on_incremental_items(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
            nonlocal hit
            hit += 1
            assert subscription.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
            assert subscription.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
            assert subscription.state == DataPackageListState.UP_TO_DATE
            if hit == 4:
                assert items == [DataPackageListItem("sek", datetime(2000, 2, 3, 4, 5, 6))]
            elif hit == 5:
                assert items == [DataPackageListItem("dkk", datetime(2000, 2, 4, 4, 5, 6))]
            elif hit == 6:
                assert items == [DataPackageListItem("usgdp", datetime(2000, 2, 5, 4, 5, 6))]
            else:
                raise Exception("should not be here")

        def on_incremental_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(7)
            assert is_aborted is False
            assert exception is None

    json = get_json(DataPackageListState.UP_TO_DATE)

    api = WebApi(Session("", "", test_auth2_session=TestAuth2Session([bytes(json, "utf-8")])))

    with pytest.raises(Exception, match="End of test"):
        _TestDataPackageListPoller(
            api,
            download_full_list_on_or_after=datetime(3000, 1, 1, tzinfo=timezone.utc),
            time_stamp_for_if_modified_since=datetime(1000, 1, 1, tzinfo=timezone.utc),
            chunk_size=1,
        ).start()

    assert hit == 8


# _run_listing and _run_listing_incomplete
def test_listing_and_listing_incomplete() -> None:
    hit = 0

    def hit_test(now: int) -> None:
        nonlocal hit
        hit += 1
        assert hit == now

    class _TestDataPackageListPoller(TestDataPackageListPoller):
        __test__ = False

        def _test_access(self) -> None:
            hit_test(1)

        def sleep(self, secs: float) -> None:
            nonlocal hit
            hit += 1
            if hit == 7:
                assert secs == self.incomplete_delay
            elif hit == 12:
                assert secs == self.up_to_date_delay
                raise Exception("End of test")
            else:
                raise Exception("should not be here")

        def now(self) -> datetime:
            hit_test(2)
            return datetime(2000, 1, 1, tzinfo=timezone.utc)

        def on_incremental_start(self, subscription: "DataPackageBody") -> None:
            nonlocal hit
            hit += 1
            assert subscription.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
            assert subscription.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
            if hit == 3:
                assert subscription.state == DataPackageListState.INCOMPLETE
            else:
                assert subscription.state == DataPackageListState.UP_TO_DATE

        def on_incremental_items(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
            nonlocal hit
            hit += 1
            assert subscription.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
            assert subscription.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
            if hit == 4:
                assert subscription.state == DataPackageListState.INCOMPLETE
                assert items == [DataPackageListItem("sek", datetime(2000, 2, 3, 4, 5, 6))]
            elif hit == 5:
                assert subscription.state == DataPackageListState.INCOMPLETE
                assert items == [DataPackageListItem("dkk", datetime(2000, 2, 4, 4, 5, 6))]
            elif hit == 6:
                assert subscription.state == DataPackageListState.INCOMPLETE
                assert items == [DataPackageListItem("usgdp", datetime(2000, 2, 5, 4, 5, 6))]
            elif hit == 8:
                assert subscription.state == DataPackageListState.UP_TO_DATE
                assert items == [DataPackageListItem("sek", datetime(2000, 2, 3, 4, 5, 6))]
            elif hit == 9:
                assert subscription.state == DataPackageListState.UP_TO_DATE
                assert items == [DataPackageListItem("dkk", datetime(2000, 2, 4, 4, 5, 6))]
            elif hit == 10:
                assert subscription.state == DataPackageListState.UP_TO_DATE
                assert items == [DataPackageListItem("usgdp", datetime(2000, 2, 5, 4, 5, 6))]
            else:
                raise Exception("should not be here")

        def on_incremental_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
            hit_test(11)
            assert is_aborted is False
            assert exception is None

    content = [
        bytes(get_json(DataPackageListState.INCOMPLETE), "utf-8"),
        bytes(get_json(DataPackageListState.UP_TO_DATE), "utf-8"),
    ]

    api = WebApi(Session("", "", test_auth2_session=TestAuth2Session(content)))

    with pytest.raises(Exception, match="End of test"):
        _TestDataPackageListPoller(
            api,
            download_full_list_on_or_after=datetime(3000, 1, 1, tzinfo=timezone.utc),
            time_stamp_for_if_modified_since=datetime(1000, 1, 1, tzinfo=timezone.utc),
            chunk_size=1,
        ).start()

    assert hit == 12
