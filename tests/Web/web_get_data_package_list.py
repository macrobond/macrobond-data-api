from datetime import datetime
from json import dumps as json_dumps
from typing import Any

from requests import Response

import pytest

from macrobond_data_api.web import WebApi
from macrobond_data_api.web.session import Session
from macrobond_data_api.web.web_types import DataPackageListItem, DataPackageListState


class TestAuth2Session:
    __test__ = False

    def __init__(self, content: bytes):
        self.content = content

    def request(self, *args: Any, **kwargs: Any) -> Response:  # pylint: disable=unused-argument
        response = Response()
        response.status_code = 200
        response._content = self.content
        return response


@pytest.mark.parametrize(
    "state",
    [DataPackageListState.FULL_LISTING, DataPackageListState.INCOMPLETE, DataPackageListState.UP_TO_DATE],
)
def test(state: DataPackageListState) -> None:
    json = json_dumps(
        {
            "downloadFullListOnOrAfter": "2000-02-01T04:05:06",
            "timeStampForIfModifiedSince": "2000-02-02T04:05:06",
            "state": state,
            "entities": [
                {"name": "sek", "modified": "2000-02-03T04:05:06"},
                {"name": "dkk", "modified": "2000-02-04T04:05:06"},
            ],
        }
    )

    api = WebApi(Session("", "", test_auth2_session=TestAuth2Session(bytes(json, "utf-8"))))

    r = api.get_data_package_list()

    assert r.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
    assert r.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
    assert r.state == state
    assert r.items == [
        DataPackageListItem("sek", datetime(2000, 2, 3, 4, 5, 6)),
        DataPackageListItem("dkk", datetime(2000, 2, 4, 4, 5, 6)),
    ]
