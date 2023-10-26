from datetime import datetime
from typing import Any, List, Optional

import pytest

from requests import Response

from macrobond_data_api.web import WebApi
from macrobond_data_api.web.data_package_list_poller import DataPackageListPoller, ExceptionSource
from macrobond_data_api.web.session import Session
from macrobond_data_api.web.web_types import DataPackageBody, DataPackageListItem


class TestAuth2Session:
    __test__ = False

    def __init__(self, *responses: Response):
        self.index = 0
        self.responses = responses

    def request(self, *args: Any, **kwargs: Any) -> Response:  # pylint: disable=unused-argument
        response = self.responses[self.index]
        self.index += 1
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


def test_access() -> None:
    hit = 0

    def hit_test(*now: int) -> int:
        nonlocal hit
        hit += 1
        assert hit in now
        return hit

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
