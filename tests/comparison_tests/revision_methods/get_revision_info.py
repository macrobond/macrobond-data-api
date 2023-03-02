import pytest
from pandas.testing import assert_frame_equal  # type: ignore

from macrobond_data_api.web import WebApi
from macrobond_data_api.com import ComApi

test_data = ["ustrad4488", "usgdp", "uscpi", "ct_au_e_ao_c_22_v", "wocaes0868"]


@pytest.mark.parametrize("name", test_data)
def test_1(name: str, web: WebApi, com: ComApi) -> None:
    web_r = web.get_revision_info(name)[0]
    com_r = com.get_revision_info(name)[0]

    assert_frame_equal(web_r.to_pd_data_frame(), com_r.to_pd_data_frame())

    assert web_r == com_r
