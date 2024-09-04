from datetime import datetime
from typing import Any, Dict

import pytest

from macrobond_data_api.web.web_types import DataPackageListState

from ..mock_adapter_builder import MAB


def get_json(state: DataPackageListState) -> Dict[Any, Any]:
    return {
        "downloadFullListOnOrAfter": "2000-02-01T04:05:06",
        "timeStampForIfModifiedSince": "2000-02-02T04:05:06",
        "state": state,
        "entities": [
            {"name": "sek", "modified": "2000-02-03T04:05:06"},
            {"name": "dkk", "modified": "2000-02-04T04:05:06"},
        ],
    }


@pytest.mark.no_account
@pytest.mark.parametrize(
    "state",
    [DataPackageListState.FULL_LISTING, DataPackageListState.INCOMPLETE, DataPackageListState.UP_TO_DATE],
)
def test_1(state: DataPackageListState, mab: MAB) -> None:
    hitponts = 1

    _, web_api, _, _ = mab.auth().get_data_package_list(get_json(state)).build()

    with web_api.get_data_package_list_chunked() as context:
        assert context.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
        assert context.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
        assert context.state == state

        assert list(context.items) == [
            [("sek", datetime(2000, 2, 3, 4, 5, 6)), ("dkk", datetime(2000, 2, 4, 4, 5, 6))],
        ]

        hitponts -= 1

    assert hitponts == 0


@pytest.mark.no_account
@pytest.mark.parametrize(
    "state",
    [DataPackageListState.FULL_LISTING, DataPackageListState.INCOMPLETE, DataPackageListState.UP_TO_DATE],
)
def test_2(state: DataPackageListState, mab: MAB) -> None:
    hitponts = 1

    _, web_api, _, _ = mab.auth().get_data_package_list(get_json(state)).build()

    with web_api.get_data_package_list_chunked(chunk_size=1) as context:
        assert context.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
        assert context.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
        assert context.state == state

        assert list(context.items) == [
            [("sek", datetime(2000, 2, 3, 4, 5, 6))],
            [("dkk", datetime(2000, 2, 4, 4, 5, 6))],
        ]

        hitponts -= 1

    assert hitponts == 0
