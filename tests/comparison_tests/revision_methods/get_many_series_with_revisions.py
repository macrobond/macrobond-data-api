from typing import Any, List
from datetime import datetime, timezone, timedelta
import pytest
from macrobond_data_api.common.types import RevisionHistoryRequest
from macrobond_data_api.common.enums import StatusCode
from macrobond_data_api.web import WebApi
from macrobond_data_api.com import ComApi


# test data of 3 first and 3 last
@pytest.fixture(scope="module", name="test_data")
def _test_data(com: ComApi) -> Any:
    data = com.get_all_vintage_series("usgdp").series
    ret = list(data[:3])
    for x in data[-3:]:
        ret.append(x)
    yield ret


@pytest.fixture(scope="module", name="test_data_2")
def _test_data_2(com: ComApi) -> Any:
    yield com.get_one_series("imffdi_218_fd_fie_ix")


@pytest.fixture(scope="module", name="test_revision_history_request")
def _test_revision_history_request(web: WebApi, com: ComApi, test_metadata: Any) -> Any:
    def test(
        request: RevisionHistoryRequest,
        status_code: StatusCode,
        include_not_modified: bool = True,
        results_len: int = 1,
    ) -> None:
        web_list = list(web.get_many_series_with_revisions([request], include_not_modified))
        com_list = list(com.get_many_series_with_revisions([request], include_not_modified))

        assert len(web_list) == len(com_list)

        assert len(web_list) == results_len

        for web_r, com_r in zip(web_list, com_list):
            test_metadata(web_r, com_r, can_be_none=True)

            assert com_r.status_code == web_r.status_code
            assert com_r.status_code == status_code

            assert len(com_r.vintages) == len(web_r.vintages)
            assert com_r.vintages[:1] == web_r.vintages[:1]
            assert com_r.vintages[-1:] == web_r.vintages[-1:]

            assert com_r == web_r

    return test


@pytest.mark.parametrize(
    "requests",
    [
        [],
        [RevisionHistoryRequest("usgdp")],
        [RevisionHistoryRequest("usgdp", if_modified_since=datetime(1, 1, 1, tzinfo=timezone.utc))],
        [RevisionHistoryRequest("usgdp", if_modified_since=datetime(9000, 1, 1, tzinfo=timezone.utc))],
        [RevisionHistoryRequest("usgdp", last_revision=datetime(1, 1, 1, tzinfo=timezone.utc))],
        [RevisionHistoryRequest("usgdp", last_revision=datetime(9000, 1, 1, tzinfo=timezone.utc))],
        [RevisionHistoryRequest("usgdp", last_revision_adjustment=datetime(1, 1, 1, tzinfo=timezone.utc))],
        [RevisionHistoryRequest("usgdp", last_revision_adjustment=datetime(9000, 1, 1, tzinfo=timezone.utc))],
    ],
    ids=[
        "[]",
        '[RevisionHistoryRequest("usgdp")]',
        "if modified since = datetime(1, 1, 1)",
        "if_modified_since = datetime(9000, 1, 1)",
        "last revision = datetime(1, 1, 1)",
        "last revision = datetime(9000, 1, 1)",
        "last revision adjustment = datetime(1, 1, 1)",
        "last revision adjustment = datetime(9000, 1, 1)",
    ],
)
def test_out_liers(requests: List[RevisionHistoryRequest], web: WebApi, com: ComApi) -> None:
    for web_r, com_r in zip(
        list(web.get_many_series_with_revisions(requests)), list(com.get_many_series_with_revisions(requests))
    ):
        web_r.metadata = {}
        com_r.metadata = {}

        assert com_r.status_code == web_r.status_code

        assert len(com_r.vintages) == len(com_r.vintages)

        assert com_r == web_r


def test_1(test_data: Any, test_revision_history_request: Any) -> None:
    """
    Test that we get the same result (no data) when we pass the current last modification timestamp
    """
    for vintage in test_data:
        metadata = vintage.metadata
        request = RevisionHistoryRequest(metadata["PrimName"], if_modified_since=metadata["LastModifiedTimeStamp"])
        test_revision_history_request(request, StatusCode.NOT_MODIFIED, include_not_modified=True)
        test_revision_history_request(request, StatusCode.OK, include_not_modified=False, results_len=0)


def test_2(test_data: Any, test_revision_history_request: Any) -> None:
    """
    Test that we get the same result (all data) when we pass an older last modification timestamp
    """
    for vintage in test_data:
        metadata = vintage.metadata
        request = RevisionHistoryRequest(
            metadata["PrimName"], if_modified_since=metadata["LastModifiedTimeStamp"] - timedelta(seconds=1)
        )
        test_revision_history_request(request, StatusCode.OK)


def test_3(test_data: Any, test_revision_history_request: Any) -> None:
    """
    Since neither the last_revision_time is now and historical timestamp, we should get incremental updates
    """
    # test_data test_data[1:] is for skipping first we.
    for vintage in test_data[1:]:
        metadata = vintage.metadata
        request = RevisionHistoryRequest(
            metadata["PrimName"],
            if_modified_since=metadata["LastModifiedTimeStamp"] - timedelta(seconds=1),
            last_revision_adjustment=metadata["LastRevisionAdjustmentTimeStamp"],
            last_revision=vintage.revision_time_stamp,
        )
        test_revision_history_request(request, StatusCode.PARTIAL_CONTENT)


def test_4(test_data: Any, test_revision_history_request: Any) -> None:
    """
    Since the last_revision_adjustment is now changed, we should get all the revisions
    """
    for vintage in test_data:
        metadata = vintage.metadata
        request = RevisionHistoryRequest(
            metadata["PrimName"],
            if_modified_since=metadata["LastModifiedTimeStamp"] - timedelta(seconds=1),
            last_revision_adjustment=metadata["LastRevisionAdjustmentTimeStamp"] - timedelta(seconds=1),
            last_revision=vintage.revision_time_stamp,
        )
        test_revision_history_request(request, StatusCode.OK)


def test_5(test_data: Any, test_revision_history_request: Any) -> None:
    metadata = test_data[0].metadata
    request = RevisionHistoryRequest(metadata["PrimName"])
    test_revision_history_request(request, StatusCode.OK)


def test_6(test_data_2: Any, test_revision_history_request: Any) -> None:
    metadata = test_data_2.metadata
    request = RevisionHistoryRequest(metadata["PrimName"])
    test_revision_history_request(request, StatusCode.OK)


def test_7(test_data_2: Any, test_revision_history_request: Any) -> None:
    metadata = test_data_2.metadata
    request = RevisionHistoryRequest(
        metadata["PrimName"],
        if_modified_since=metadata["LastModifiedTimeStamp"] + timedelta(seconds=1),
    )
    test_revision_history_request(request, StatusCode.NOT_MODIFIED)


def test_8(test_data_2: Any, test_revision_history_request: Any) -> None:
    metadata = test_data_2.metadata
    request = RevisionHistoryRequest(
        metadata["PrimName"],
        if_modified_since=metadata["LastModifiedTimeStamp"] + timedelta(seconds=1),
    )
    test_revision_history_request(request, None, include_not_modified=False, results_len=0)


def test_9(test_data_2: Any, test_revision_history_request: Any) -> None:
    metadata = test_data_2.metadata
    request = RevisionHistoryRequest(
        metadata["PrimName"],
        if_modified_since=metadata["LastModifiedTimeStamp"],
        last_revision=metadata["LastRevisionTimeStamp"] + timedelta(seconds=1),
    )
    test_revision_history_request(request, StatusCode.NOT_MODIFIED)


def test_10(test_revision_history_request: Any) -> None:
    request = RevisionHistoryRequest("bad name")
    test_revision_history_request(request, StatusCode.NOT_FOUND)


# TODO @mb-jp uese this test ?
# def test_11(web: WebApi, com: ComApi) -> None:
#    requests = [RevisionHistoryRequest("usgdp"), RevisionHistoryRequest("usgdp"), RevisionHistoryRequest("name")]
#
#    with pytest.raises(ValueError, match=""):
#        web.get_many_series_with_revisions(requests)
#
#    with pytest.raises(ValueError, match=""):
#        com.get_many_series_with_revisions(requests)
