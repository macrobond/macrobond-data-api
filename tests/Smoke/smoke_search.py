import pytest
from macrobond_data_api.common.types import SearchFilter
from macrobond_data_api.common import Api


@pytest.mark.usefixtures("assert_no_warnings")
@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test(api: Api) -> None:  # pylint: disable=unused-argument
    # Entity_search
    result1 = api.entity_search("usgdp")
    result1.to_pd_data_frame()
    result1.to_dict()

    # Entity_search_multi_filter
    result2 = api.entity_search_multi_filter(SearchFilter("usgdp"))
    result2.to_pd_data_frame()
    result2.to_dict()
