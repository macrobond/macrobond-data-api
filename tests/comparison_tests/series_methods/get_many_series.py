from typing import Any, List, Tuple, cast, Generator, Optional, Union
from datetime import datetime, timedelta, timezone
import pytest
from macrobond_data_api.web import WebApi
from macrobond_data_api.com import ComApi


@pytest.fixture(scope="module", name="test_data")
def _test_data(com: ComApi) -> Generator[List[Tuple[bool, Union[str, Tuple[str, Optional[datetime]]]]], None, None]:
    usgdp_time_stamps = [
        cast(datetime, x.metadata["LastModifiedTimeStamp"]) for x in com.get_all_vintage_series("usgdp")
    ]

    imffdi_time_stamps = cast(datetime, com.get_one_series("imffdi_218_fd_fie_ix").metadata["LastModifiedTimeStamp"])

    yield [
        (False, ("usgdp", (usgdp_time_stamps[:1][0] - timedelta(seconds=1)))),
        (True, ("usgdp", usgdp_time_stamps[:1][0])),
        (True, ("usgdp", usgdp_time_stamps[-1:][0])),
        (True, ("usgdp", None)),
        (True, "usgdp"),
        (True, ("imffdi_218_fd_fie_ix", imffdi_time_stamps - timedelta(seconds=1))),
        (True, ("imffdi_218_fd_fie_ix", imffdi_time_stamps)),
        (True, ("imffdi_218_fd_fie_ix", None)),
        (True, ("bad name", imffdi_time_stamps)),
        (True, ("bad name", None)),
        (True, "bad name"),
    ]


index_list = list(range(11))


@pytest.mark.parametrize("index_", index_list)
def test_1(index_: Any, web: WebApi, com: ComApi, test_data: Any, test_metadata: Any) -> None:
    assert len(index_list) == len(test_data)

    can_be_empty = test_data[index_][0]
    series = test_data[index_][1:]

    web_list = list(web.get_many_series(series))
    com_list = list(com.get_many_series(series))

    for web_r, com_r in zip(web_list, com_list):
        test_metadata(web_r, com_r, can_be_empty=can_be_empty)

        assert web_r == com_r


@pytest.mark.parametrize("index_", index_list)
def test_2(index_: Any, web: WebApi, com: ComApi, test_data: Any, test_metadata: Any) -> None:
    assert len(index_list) == len(test_data)

    can_be_empty = test_data[index_][0]
    series = test_data[index_][1:]

    web_list = list(web.get_many_series(series, include_not_modified=True))
    com_list = list(com.get_many_series(series, include_not_modified=True))

    for web_r, com_r in zip(web_list, com_list):
        test_metadata(web_r, com_r, can_be_empty=can_be_empty)

        assert web_r == com_r


@pytest.mark.parametrize(
    "name",
    ["usgdp", "imffdi_218_fd_fie_ix"],
)
def test_3(name: str, web: WebApi, com: ComApi) -> None:
    series = [(name, datetime(3000, 1, 1, tzinfo=timezone.utc))]
    web_list = list(web.get_many_series(series))
    com_list = list(com.get_many_series(series))

    assert len(web_list) == len(com_list)
    assert len(web_list) == 0


@pytest.mark.parametrize(
    "name",
    ["usgdp", "imffdi_218_fd_fie_ix"],
)
def test_4(name: str, web: WebApi, com: ComApi) -> None:
    series = [(name, datetime(3000, 1, 1, tzinfo=timezone.utc))]
    web_list = list(web.get_many_series(series, include_not_modified=True))
    com_list = list(com.get_many_series(series, include_not_modified=True))

    assert len(web_list) == len(com_list)
    assert len(web_list) == 1


def test_5(web: WebApi, com: ComApi) -> None:
    series: List[Tuple[str, datetime]] = [
        ("Name", datetime(1, 2, 3)),
        ("usgdp", datetime(1, 2, 3)),
        ("usgdp", datetime(1, 2, 3)),
    ]

    text = "duplicate of series"

    with pytest.raises(ValueError, match=text):
        list(web.get_many_series(series))

    with pytest.raises(ValueError, match=text):
        list(com.get_many_series(series))
