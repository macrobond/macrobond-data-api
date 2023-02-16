import pytest
from macrobond_data_api.com import ComApi
from macrobond_data_api.web import WebApi
from macrobond_data_api.common import Api
from macrobond_data_api.common.types import SearchFilter, StartOrEndPoint


class TestCommon:
    def test_start_or_end_point(self) -> None:
        assert repr(StartOrEndPoint.relative_to_observations(-1)) == "-1 mode:CalendarDateMode.DATA_IN_ANY_SERIES"

        assert str(StartOrEndPoint.relative_to_observations(-1)) == "-1 mode:CalendarDateMode.DATA_IN_ANY_SERIES"

        assert str(StartOrEndPoint.relative_to_years(-1)) == "-1y mode:CalendarDateMode.DATA_IN_ANY_SERIES"

        assert str(StartOrEndPoint.relative_to_quarters(-1)) == "-1q mode:CalendarDateMode.DATA_IN_ANY_SERIES"

        assert str(StartOrEndPoint.relative_to_months(-1)) == "-1m mode:CalendarDateMode.DATA_IN_ANY_SERIES"

        assert str(StartOrEndPoint.relative_to_weeks(-1)) == "-1w mode:CalendarDateMode.DATA_IN_ANY_SERIES"

        assert str(StartOrEndPoint.relative_to_days(-1)) == "-1d mode:CalendarDateMode.DATA_IN_ANY_SERIES"

        assert str(StartOrEndPoint("-1", None)) == "-1 mode:CalendarDateMode.DATA_IN_ANY_SERIES"

        assert str(StartOrEndPoint.data_in_all_series()) == " mode:CalendarDateMode.DATA_IN_ALL_SERIES"

        assert str(StartOrEndPoint.data_in_any_series()) == " mode:CalendarDateMode.DATA_IN_ANY_SERIES"

    def test_series_multi_filter(self, web: WebApi, com: ComApi) -> None:
        com_r = com.entity_search_multi_filter(SearchFilter(text="usgdp"))
        web_r = web.entity_search_multi_filter(SearchFilter(text="usgdp"))

        assert len(com_r) == len(web_r)

        assert len(com_r) != 0

        com_first = com_r[0]
        web_first = web_r[0]

        assert com_first.get("PrimName") == web_first.get("PrimName")
        assert com_first.get("PrimName") is not None
        assert com_first.get("PrimName") != ""


def test_web_search_no_metadata(web: WebApi) -> None:
    search_result = web.entity_search(text="usgdp", no_metadata=True)

    assert len(search_result) != 0, "len(search_result) != 0"
    first = search_result[0]

    assert len(first) == 1, "len(first)"


def test_com_search_no_metadata(com: ComApi) -> None:
    search_result = com.entity_search(text="usgdp", no_metadata=True)

    assert len(search_result) != 0, "len(search_result) != 0"
    first = search_result[0]

    assert len(first) != 1, "len(first)"


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_search(api: Api) -> None:
    search_result = api.entity_search(text="usgdp")

    assert len(search_result) != 0, "len(search_result) != 0"
    first = search_result[0]

    assert len(first) != 0, "len(first)"


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_series_multi_filter(api: Api) -> None:
    search_result = api.entity_search_multi_filter(SearchFilter(text="usgdp"))

    assert len(search_result) != 0, "len(search_result) != 0"
    first = search_result[0]

    assert len(first) != 0, "len(first)"


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_series_multi_filter_must_have_attributes(api: Api) -> None:
    search_result = api.entity_search_multi_filter(SearchFilter(must_have_attributes=["MoveBase"]))

    assert len(search_result) != 0, "len(search_result) != 0"

    for entitie in search_result:
        assert "MoveBase" in entitie, "MoveBase not in " + str(entitie)


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_series_multi_filter_must_not_have_attributes(api: Api) -> None:
    search_result = api.entity_search_multi_filter(SearchFilter("abc", must_not_have_attributes=["MoveBase"]))

    assert len(search_result) != 0, "len(com.entities) != 0"

    for entitie in search_result:
        assert "MoveBase" not in entitie, "MoveBase is in " + str(entitie)


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_series_multi_filter_must_have_values(api: Api) -> None:
    search_result = api.entity_search_multi_filter(SearchFilter(must_have_values={"MoveBase": "pp100"}))

    assert len(search_result) != 0, "len(com) != 0"

    for entitie in search_result:
        assert entitie.get("MoveBase") == "pp100", 'MoveBase != "pp100" ' + str(entitie)


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_series_multi_filter_must_not_have_values(api: Api) -> None:
    search_result = api.entity_search_multi_filter(SearchFilter("abc", must_not_have_values={"MoveBase": "pp100"}))

    assert len(search_result) != 0, "len(com.entities) != 0"

    for entitie in search_result:
        assert entitie.get("MoveBase") != "pp100", 'MoveBase != "pp100" ' + str(entitie)


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_series_multi_filter_include_discontinued(api: Api) -> None:
    text = "s_07707"

    include = api.entity_search_multi_filter(
        SearchFilter(text=text),
        include_discontinued=True,
    )

    not_include = api.entity_search_multi_filter(
        SearchFilter(text=text),
        include_discontinued=False,
    )

    assert len(include) != 6000, "len(include) != 6000"
    assert len(not_include) != 6000, "len(not_include) != 6000"

    assert len(include) != 0, "len(include) != 0"
    assert len(not_include) != 0, "len(not_include) != 0"

    assert len(include) > len(not_include), "include > not_include"


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_series_multi_filter_entity_types(api: Api) -> None:
    text = "abc"

    security = api.entity_search_multi_filter(SearchFilter(text=text, entity_types=["Security"]))

    assert len(security) != 0, "len(security) != 0"

    for entitie in security:
        assert entitie.get("EntityType") == "Security"
