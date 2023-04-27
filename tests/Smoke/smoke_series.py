from typing import List

import pytest  # type: ignore[attr-defined]
from macrobond_data_api.web.web_types import DataPackageBody, DataPackageListItem
from macrobond_data_api.common import Api
from macrobond_data_api.web import WebApi
from macrobond_data_api.common.types import RevisionHistoryRequest


@pytest.mark.usefixtures("assert_no_warnings")
@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test(api: Api) -> None:  # pylint: disable=unused-argument
    # Get_one_series
    result1 = api.get_one_series("usgdp")
    str(result1.values_to_pd_data_frame())
    result1.to_dict()

    # Get_series
    result2 = api.get_series(["usgdp"])[0]
    str(result2.values_to_pd_data_frame())
    result2.to_dict()

    # Get_one_entity
    result3 = api.get_one_entity("usgdp")
    str(result3.metadata_to_pd_series())
    result3.to_dict()

    # Get_entities
    result4 = api.get_entities(["usgdp"])[0]
    str(result4.metadata_to_pd_series())
    result4.to_dict()

    # Get_unified_series
    result5 = api.get_unified_series("usgdp", "uscpi")
    str(result5.to_pd_data_frame())
    result5.to_dict()


class TestWeb:
    @pytest.mark.usefixtures("assert_no_warnings")
    def test_get_data_package_list(self, web: WebApi) -> None:
        pytest.skip("needs access")
        result = web.get_data_package_list()  # pylint: disable=unused-variable
        breakpoint()  # pylint: disable=forgotten-debug-statement

    @pytest.mark.usefixtures("assert_no_warnings")
    def test_get_data_package_list_iterative(self, web: WebApi) -> None:
        pytest.skip("needs access")

        def empty_method_1(body: DataPackageBody) -> bool:  # pylint: disable=unused-argument
            return True

        def empty_method_2(
            body: DataPackageBody,  # pylint: disable=unused-argument
            items: List[DataPackageListItem],  # pylint: disable=unused-argument
        ) -> bool:
            return True

        web.get_data_package_list_iterative(empty_method_1, empty_method_2)

    @pytest.mark.usefixtures("assert_no_warnings")
    @pytest.mark.parametrize("api", ["web", "com"], indirect=True)
    def test_get_many_series_with_revisions(self, api: Api) -> None:
        pytest.skip("needs access")

        for _ in api.get_many_series_with_revisions([RevisionHistoryRequest("usgdp"), RevisionHistoryRequest("uscpi")]):
            ...
