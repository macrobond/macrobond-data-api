from typing import Any
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal
from macrobond_data_api.web import WebApi
from macrobond_data_api.com import ComApi

test_data = ["ustrad4488", "usgdp", "uscpi", "ct_au_e_ao_c_22_v", "wocaes0868"]


@pytest.mark.parametrize("name", test_data)
def test_1(name: str, web: WebApi, com: ComApi, test_metadata: Any) -> None:
    web_r = web.get_one_series(name)
    com_r = com.get_one_series(name)

    test_metadata(web_r, com_r)

    assert web_r == com_r


@pytest.mark.parametrize("name", test_data)
def test_2(name: str, web: WebApi, com: ComApi, test_metadata: Any) -> None:
    web_r = web.get_one_series(name)
    com_r = com.get_one_series(name)

    test_metadata(web_r, com_r)

    assert_frame_equal(web_r.values_to_pd_data_frame(), com_r.values_to_pd_data_frame())


@pytest.mark.parametrize("name", test_data)
def test_3(name: str, web: WebApi, com: ComApi, test_metadata: Any) -> None:
    web_r = web.get_one_series(name)
    com_r = com.get_one_series(name)

    test_metadata(web_r, com_r)

    assert_series_equal(web_r.metadata_to_pd_series(), com_r.metadata_to_pd_series())
