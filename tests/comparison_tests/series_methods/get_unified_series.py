from typing import Any
import pytest
from pandas.testing import assert_frame_equal  # type: ignore

from macrobond_data_api.web import WebApi
from macrobond_data_api.com import ComApi

test_data = ["ustrad4488", "usgdp", "uscpi", "ct_au_e_ao_c_22_v", "wocaes0868"]


@pytest.mark.parametrize("name", test_data)
def test_1(name: str, web: WebApi, com: ComApi, test_metadata: Any) -> None:
    web_r = web.get_unified_series(name)
    com_r = com.get_unified_series(name)

    test_metadata(web_r.series, com_r.series)

    assert_frame_equal(web_r.to_pd_data_frame(), com_r.to_pd_data_frame())

    assert web_r == com_r


def test_2(web: WebApi, com: ComApi, test_metadata: Any) -> None:
    web_r = web.get_unified_series(*test_data)
    com_r = com.get_unified_series(*test_data)

    test_metadata(web_r.series, com_r.series)

    assert_frame_equal(web_r.to_pd_data_frame(), com_r.to_pd_data_frame())

    assert web_r == com_r
