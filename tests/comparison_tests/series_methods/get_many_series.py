from typing import Any, List, Tuple, cast, Generator
from datetime import datetime, timedelta
import pytest
from macrobond_data_api.web import WebApi
from macrobond_data_api.com import ComApi


@pytest.fixture(scope="module", name="test_data")
def _test_data(com: ComApi) -> Generator[List[Tuple[str, datetime]], None, None]:
    usgdp_time_stamps = [
        cast(datetime, x.metadata["LastModifiedTimeStamp"]) for x in com.get_all_vintage_series("usgdp")
    ]

    imffdi_time_stamps = cast(datetime, com.get_one_series("imffdi_218_fd_fie_ix").metadata["LastModifiedTimeStamp"])

    yield [
        ("usgdp", (usgdp_time_stamps[:1][0] - timedelta(seconds=1))),
        ("usgdp", usgdp_time_stamps[:1][0]),
        ("usgdp", usgdp_time_stamps[-1:][0]),
        ("imffdi_218_fd_fie_ix", imffdi_time_stamps - timedelta(seconds=1)),
        ("imffdi_218_fd_fie_ix", imffdi_time_stamps),
        ("bad name", imffdi_time_stamps),
    ]


@pytest.mark.parametrize("data", [(0, False), (1, True), (2, True), (3, True), (4, True), (5, True)])
def test_1(data: Any, web: WebApi, com: ComApi, test_data: Any, test_metadata: Any) -> None:
    series = test_data[data[0]]

    web_list = list(web.get_many_series(series))
    com_list = list(com.get_many_series(series))

    for web_r, com_r in zip(web_list, com_list):
        test_metadata(web_r, com_r, can_be_empty=data[1])

        assert web_r == com_r


def test_2(web: WebApi, com: ComApi) -> None:
    series: List[Tuple[str, datetime]] = [
        ("Name", datetime(1, 2, 3)),
        ("usgdp", datetime(1, 2, 3)),
        ("usgdp", datetime(1, 2, 3)),
    ]

    text = "duplicate of series"

    with pytest.raises(ValueError, match=text):
        list(web.get_many_series(*series))

    with pytest.raises(ValueError, match=text):
        list(com.get_many_series(*series))
