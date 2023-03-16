from pandas import DataFrame  # type: ignore
from pandas.testing import assert_frame_equal  # type: ignore

import pytest

from macrobond_data_api.common import Api
from macrobond_data_api.com import ComApi
from macrobond_data_api.web import WebApi
from macrobond_data_api.common.types import GetEntitiesError, SeriesEntry


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_get_one_series(api: Api) -> None:
    series = api.get_one_series("usgdp")
    assert series.is_error is False

    assert len(series.values) != 0
    assert len(series.dates) != 0
    assert len(series.dates) == len(series.values)

    assert series.entity_type == "TimeSeries"

    assert isinstance(series.values[0], float)

    series = api.get_one_series("noseries!", raise_error=False)
    assert series.is_error is True
    assert series.error_message == "Not found"

    # test raise_get_entities_error=True

    with pytest.raises(GetEntitiesError, match="failed to retrieve:\n\tnoseries! error_message: Not found"):
        api.get_one_series("noseries!")


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_get_series(api: Api) -> None:
    series = api.get_series("usgdp", "uscpi", "noseries!", raise_error=False)

    # test.assertEqual(series[0].name, 'usgdp', 'name')
    assert series[0].primary_name == "usnaac0169"
    assert series[0].is_error is False
    assert series[0].error_message == ""
    assert isinstance(series[0].values[0], float)

    # test.assertEqual(series[1].name, 'uscpi', 'name')
    assert series[1].primary_name == "uspric2156"
    assert series[1].is_error is False
    assert series[1].error_message == ""

    # test.assertEqual(series[2].name, 'noseries!', 'name')
    # test.assertEqual(series[2].primary_name, '', 'primary_name')
    assert series[2].is_error is True
    assert series[2].error_message == "Not found"

    # test raise_get_entities_error=True

    with pytest.raises(GetEntitiesError, match="failed to retrieve:\n\tnoseries! error_message: Not found"):
        api.get_series("usgdp", "noseries!")


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_get_one_entity(api: Api) -> None:
    entitie = api.get_one_entity("usgdp")
    # test.assertEqual(entitie.name, 'usgdp', 'name')
    assert entitie.primary_name == "usnaac0169"
    assert entitie.is_error is False
    assert entitie.error_message == ""
    assert entitie.metadata is not None

    entitie = api.get_one_entity("noseries!", raise_error=False)
    # test.assertEqual(entitie.name, 'noseries!', 'name')
    assert entitie.is_error is True
    assert entitie.error_message == "Not found"

    # test raise_get_entities_error=True

    with pytest.raises(GetEntitiesError, match="failed to retrieve:\n\tnoseries! error_message: Not found"):
        api.get_one_entity("noseries!")

    # dict

    dict_series = api.get_one_entity("usgdp", raise_error=False).to_dict()

    assert dict_series["Name"] == "usgdp"
    assert dict_series["metadata.Class"] == "stock"

    # test is_discontinued

    assert api.get_one_entity("uslama9621").is_discontinued is True

    assert api.get_one_entity("usgdp").is_discontinued is False


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_get_entities(api: Api) -> None:
    entities = api.get_entities("usgdp", "uscpi", "noseries!", raise_error=False)

    # test.assertEqual(series[0].name, 'usgdp', 'name')
    assert entities[0].primary_name == "usnaac0169"
    assert entities[0].is_error is False
    assert entities[0].error_message == ""

    # test.assertEqual(series[1].name, 'uscpi', 'name')
    assert entities[1].primary_name == "uspric2156"
    assert entities[1].is_error is False
    assert entities[1].error_message == ""

    # test.assertEqual(series[2].name, 'noseries!', 'name')
    # test.assertEqual(series[2].primary_name, '', 'primary_name')
    assert entities[2].is_error is True
    assert entities[2].error_message == "Not found"

    # test raise_get_entities_error=True

    with pytest.raises(GetEntitiesError, match="failed to retrieve:\n\tnoseries! error_message: Not found"):
        api.get_entities("usgdp", "noseries!")


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_get_unified_series_no_series(api: Api) -> None:
    unified = api.get_unified_series("noseries!", raise_error=False)

    assert unified.dates == []
    assert len(unified) == 1

    assert unified[0].is_error is True
    assert unified[0].error_message == "noseries! : Not found"
    assert unified[0].values == []

    unified = api.get_unified_series(raise_error=False)

    assert unified.dates == []
    assert len(unified) == 0

    with pytest.raises(GetEntitiesError, match="failed to retrieve:\n\tnoseries! error_message: noseries! : Not found"):
        unified = api.get_unified_series("noseries!")


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_get_unified_series_vintage(api: Api) -> None:
    revision_info = api.get_revision_info("usgdp")[0]

    unified_1 = api.get_unified_series(SeriesEntry("usgdp"))[0]

    unified_2 = api.get_unified_series(SeriesEntry("usgdp", revision_info.time_stamp_of_last_revision))[0]

    unified_3 = api.get_unified_series(SeriesEntry("usgdp", revision_info.time_stamp_of_first_revision))[0]

    assert unified_1.values == unified_2.values

    assert unified_1.values != unified_3.values


class TestCommon:
    # get_one_series

    def test_get_one_series_values_to_pd_series(self, web: WebApi, com: ComApi) -> None:
        assert_frame_equal(
            web.get_one_series("usgdp").values_to_pd_data_frame(), com.get_one_series("usgdp").values_to_pd_data_frame()
        )

        assert_frame_equal(
            web.get_one_series("ustrad4488").values_to_pd_data_frame(),
            com.get_one_series("ustrad4488").values_to_pd_data_frame(),
        )

        assert_frame_equal(
            web.get_one_series("ct_au_e_ao_c_22_v").values_to_pd_data_frame(),
            com.get_one_series("ct_au_e_ao_c_22_v").values_to_pd_data_frame(),
        )

    # get_unified_series

    def test_get_unified_series_to_pd_data_frame(self, web: WebApi, com: ComApi) -> None:
        assert 0 == len(
            DataFrame.compare(
                web.get_unified_series("usgdp").to_pd_data_frame(),
                com.get_unified_series("usgdp").to_pd_data_frame(),
            )
        )

        assert 0 == len(
            DataFrame.compare(
                web.get_unified_series("ustrad4488").to_pd_data_frame(),
                com.get_unified_series("ustrad4488").to_pd_data_frame(),
            )
        )

        assert 0 == len(
            DataFrame.compare(
                web.get_unified_series("ct_au_e_ao_c_22_v").to_pd_data_frame(),
                com.get_unified_series("ct_au_e_ao_c_22_v").to_pd_data_frame(),
            )
        )
