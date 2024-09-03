from datetime import datetime
from typing import List
import warnings

import pytest

from macrobond_data_api.web.web_types import DataPackageBody, DataPackageListItem, DataPackageListState

from ..mock_adapter_builder import MAB


@pytest.mark.no_account
@pytest.mark.parametrize(
    "state",
    [DataPackageListState.FULL_LISTING, DataPackageListState.INCOMPLETE, DataPackageListState.UP_TO_DATE],
)
def test(state: DataPackageListState, mab: MAB) -> None:
    raw = {
        "downloadFullListOnOrAfter": "2000-02-01T04:05:06",
        "timeStampForIfModifiedSince": "2000-02-02T04:05:06",
        "state": state,
        "entities": [
            {"name": "sek", "modified": "2000-02-03T04:05:06"},
            {"name": "dkk", "modified": "2000-02-04T04:05:06"},
        ],
    }

    hitponts = 2

    def body_callback(body: DataPackageBody) -> None:
        assert body.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
        assert body.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
        assert body.state == state
        nonlocal hitponts
        hitponts -= 1

    def items_callback(body: DataPackageBody, data: List[DataPackageListItem]) -> None:
        assert body.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
        assert body.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
        assert body.state == state
        assert data == [
            DataPackageListItem("sek", datetime(2000, 2, 3, 4, 5, 6)),
            DataPackageListItem("dkk", datetime(2000, 2, 4, 4, 5, 6)),
        ]
        nonlocal hitponts
        hitponts -= 1

    _, webApi, _, _ = mab.auth().get_data_package_list(raw).build()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        webApi.get_data_package_list_iterative(body_callback, items_callback)

    assert hitponts == 0
