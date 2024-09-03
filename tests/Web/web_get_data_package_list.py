from datetime import datetime

import pytest

from macrobond_data_api.web.web_types import DataPackageListItem, DataPackageListState

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

    _, webApi, _, _ = mab.auth().get_data_package_list(raw).build()

    r = webApi.get_data_package_list()

    assert r.download_full_list_on_or_after == datetime(2000, 2, 1, 4, 5, 6)
    assert r.time_stamp_for_if_modified_since == datetime(2000, 2, 2, 4, 5, 6)
    assert r.state == state
    assert r.items == [
        DataPackageListItem("sek", datetime(2000, 2, 3, 4, 5, 6)),
        DataPackageListItem("dkk", datetime(2000, 2, 4, 4, 5, 6)),
    ]
