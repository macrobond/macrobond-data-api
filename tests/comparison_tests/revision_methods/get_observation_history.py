from datetime import datetime
from typing import Optional
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal

from macrobond_data_api.web import WebApi
from macrobond_data_api.com import ComApi

test_data = ["ustrad4488", "usgdp", "uscpi"]


def strip_time(d: Optional[datetime]) -> Optional[datetime]:
    return datetime(d.year, d.month, d.day) if d else None


@pytest.mark.parametrize("name", test_data)
def test_1(name: str, web: WebApi, com: ComApi) -> None:
    info = web.get_revision_info(name)[0]

    time = info.vintage_time_stamps[1]
    web_r = web.get_observation_history(name, time)[0]
    com_r = com.get_observation_history(name, time)[0]

    assert web_r.values == com_r.values

    web_r.time_stamps = [strip_time(x) for x in web_r.time_stamps]  # type: ignore
    assert web_r.time_stamps == com_r.time_stamps

    assert web_r.observation_date == com_r.observation_date

    assert_frame_equal(web_r.to_pd_data_frame(), com_r.to_pd_data_frame())

    assert_series_equal(web_r.to_pd_series(), com_r.to_pd_series())
