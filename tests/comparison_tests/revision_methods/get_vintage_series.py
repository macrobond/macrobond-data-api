from typing import Any
import pytest
from pandas.testing import assert_series_equal, assert_frame_equal  # type: ignore

from macrobond_data_api.web import WebApi
from macrobond_data_api.com import ComApi

test_data = ["ustrad4488", "usgdp", "uscpi"]


@pytest.mark.parametrize("name", test_data)
def test_1(name: str, web: WebApi, com: ComApi, test_metadata: Any) -> None:
    info = web.get_revision_info(name)[0]

    time = info.vintage_time_stamps[1]

    web_r = web.get_vintage_series(time, [name])[0]
    com_r = com.get_vintage_series(time, [name])[0]

    test_metadata(web_r, com_r)

    assert web_r == com_r


@pytest.mark.parametrize("name", test_data)
def test_2(name: str, web: WebApi, com: ComApi, test_metadata: Any) -> None:
    info = web.get_revision_info(name)[0]

    time = info.vintage_time_stamps[1]

    web_r = web.get_vintage_series(time, [name])[0]
    com_r = com.get_vintage_series(time, [name])[0]

    test_metadata(web_r, com_r)

    assert_frame_equal(web_r.values_to_pd_data_frame(), com_r.values_to_pd_data_frame())


@pytest.mark.parametrize("name", test_data)
def test_3(name: str, web: WebApi, com: ComApi, test_metadata: Any) -> None:
    info = web.get_revision_info(name)[0]

    time = info.vintage_time_stamps[1]

    web_r = web.get_vintage_series(time, [name])[0]
    com_r = com.get_vintage_series(time, [name])[0]

    test_metadata(web_r, com_r)

    assert_series_equal(web_r.metadata_to_pd_series(), com_r.metadata_to_pd_series())


@pytest.mark.parametrize("name", test_data)
def test_4(name: str, web: WebApi, com: ComApi, test_metadata: Any) -> None:
    info = web.get_revision_info(name)[0]

    time = info.vintage_time_stamps[1]

    web_r = web.get_vintage_series(time, [name], include_times_of_change=True)[0]
    com_r = com.get_vintage_series(time, [name], include_times_of_change=True)[0]

    assert web_r.values_metadata == com_r.values_metadata

    test_metadata(web_r, com_r)

    assert web_r == com_r
