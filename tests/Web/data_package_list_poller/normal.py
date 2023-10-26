from datetime import datetime, timezone
from io import BytesIO
from json import dumps as json_dumps
from typing import Any, Dict, List, Optional

import pytest

from requests import Response

from macrobond_data_api.web import WebApi
from macrobond_data_api.web.data_package_list_poller import DataPackageListPoller, ExceptionSource
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

    def on_full_listing_begin(self, subscription: "DataPackageBody") -> None:
        raise Exception("should not be called")

    def on_full_listing_batch(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
        raise Exception("should not be called")

    def on_full_listing_end(self, is_aborted: bool) -> None:
        raise Exception("should not be called")

    def on_incremental_begin(self, subscription: "DataPackageBody") -> None:
        raise Exception("should not be called")

    def on_incremental_batch(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
        raise Exception("should not be called")

    def on_incremental_end(self, is_aborted: bool) -> None:
        raise Exception("should not be called")

    def on_exception(self, source: ExceptionSource, exception: Exception) -> None:
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
            hit_test(7)
            assert secs == self.up_to_date_delay
            raise Exception("End of test")

        def on_full_listing_begin(self, subscription: "DataPackageBody") -> None:
            hit_test(2)
            assert subscription.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
            assert subscription.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
            assert subscription.state == DataPackageListState.FULL_LISTING

        def on_full_listing_batch(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
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

        def on_full_listing_end(self, is_aborted: bool) -> None:
            hit_test(6)
            assert is_aborted is False

    api = get_api(get_json_response(DataPackageListState.FULL_LISTING))

    with pytest.raises(Exception, match="End of test"):
        _TestDataPackageListPoller(api, chunk_size=1).start()

    assert hit == 7


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
            hit_test(8)
            assert secs == self.up_to_date_delay
            raise Exception("End of test")

        def now(self) -> datetime:
            hit_test(2)
            return datetime(2000, 1, 1, tzinfo=timezone.utc)

        def on_incremental_begin(self, subscription: "DataPackageBody") -> None:
            hit_test(3)
            assert subscription.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
            assert subscription.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
            assert subscription.state == DataPackageListState.UP_TO_DATE

        def on_incremental_batch(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
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

        def on_incremental_end(self, is_aborted: bool) -> None:
            hit_test(7)
            assert is_aborted is False

    api = get_api(get_json_response(DataPackageListState.UP_TO_DATE))

    with pytest.raises(Exception, match="End of test"):
        _TestDataPackageListPoller(
            api,
            download_full_list_on_or_after=datetime(3000, 1, 1, tzinfo=timezone.utc),
            time_stamp_for_if_modified_since=datetime(1000, 1, 1, tzinfo=timezone.utc),
            chunk_size=1,
        ).start()

    assert hit == 8


# _run_listing and _run_listing_incomplete
def test_listing_and_listing_incomplete_1() -> None:
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
            hit = hit_test(7, 12)
            if hit == 7:
                assert secs == self.incomplete_delay
            elif hit == 12:
                assert secs == self.up_to_date_delay
                raise Exception("End of test")

        def now(self) -> datetime:
            hit_test(2)
            return datetime(2000, 1, 1, tzinfo=timezone.utc)

        def on_incremental_begin(self, subscription: "DataPackageBody") -> None:
            assert subscription.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
            assert subscription.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
            if hit_test(3) == 3:
                assert subscription.state == DataPackageListState.INCOMPLETE

        def on_incremental_batch(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
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

        def on_incremental_end(self, is_aborted: bool) -> None:
            hit_test(11)
            assert is_aborted is False

    api = get_api(
        get_json_response(DataPackageListState.INCOMPLETE), get_json_response(DataPackageListState.UP_TO_DATE)
    )

    with pytest.raises(Exception, match="End of test"):
        _TestDataPackageListPoller(
            api,
            download_full_list_on_or_after=datetime(3000, 1, 1, tzinfo=timezone.utc),
            time_stamp_for_if_modified_since=datetime(1000, 1, 1, tzinfo=timezone.utc),
            chunk_size=1,
        ).start()

    assert hit == 12


def test_listing_and_listing_incomplete_2() -> None:
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
            hit = hit_test(5, 7, 10)
            if hit in (5, 7):
                assert secs == self.incomplete_delay
            elif hit == 10:
                assert secs == self.up_to_date_delay
                raise Exception("End of test")

        def now(self) -> datetime:
            hit_test(2)
            return datetime(2000, 1, 1, tzinfo=timezone.utc)

        def on_incremental_begin(self, subscription: "DataPackageBody") -> None:
            assert subscription.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
            assert subscription.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
            if hit_test(3) == 3:
                assert subscription.state == DataPackageListState.INCOMPLETE

        def on_incremental_batch(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
            hit = hit_test(4, 6, 8)
            assert subscription.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
            assert subscription.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)

            assert items == [
                DataPackageListItem("sek", datetime(2000, 2, 3, 4, 5, 6)),
                DataPackageListItem("dkk", datetime(2000, 2, 4, 4, 5, 6)),
                DataPackageListItem("usgdp", datetime(2000, 2, 5, 4, 5, 6)),
            ]

            if hit in (4, 6):
                assert subscription.state == DataPackageListState.INCOMPLETE
            elif hit == 8:
                assert subscription.state == DataPackageListState.UP_TO_DATE
            else:
                raise Exception("should not be here")

        def on_incremental_end(self, is_aborted: bool) -> None:
            hit_test(9)
            assert is_aborted is False

    api = get_api(
        get_json_response(DataPackageListState.INCOMPLETE),
        get_json_response(DataPackageListState.INCOMPLETE),
        get_json_response(DataPackageListState.UP_TO_DATE),
    )

    with pytest.raises(Exception, match="End of test"):
        _TestDataPackageListPoller(
            api,
            download_full_list_on_or_after=datetime(3000, 1, 1, tzinfo=timezone.utc),
            time_stamp_for_if_modified_since=datetime(1000, 1, 1, tzinfo=timezone.utc),
        ).start()

    assert hit == 10
