from typing import Any, Tuple, List
import pytest
from macrobond_data_api.common.types.get_entity_error import GetEntitiesError
from macrobond_data_api.web import WebApi
from macrobond_data_api.com import ComApi


@pytest.mark.parametrize(
    "data",
    [
        (-1, ["usgdp"]),
        (0, ["usgdp"]),
        (1, ["usgdp"]),
        (99999, ["usgdp"]),
        (-1, ["imffdi_218_fd_fie_ix"]),
        (0, ["imffdi_218_fd_fie_ix"]),
        (1, ["imffdi_218_fd_fie_ix"]),
        (-1, ["usgdp", "imffdi_218_fd_fie_ix"]),
        (0, ["usgdp", "imffdi_218_fd_fie_ix"]),
        (1, ["usgdp", "imffdi_218_fd_fie_ix"]),
        (-1, ["usgdp", "imffdi_218_fd_fie_ix", "usgdp"]),
        (0, ["usgdp", "imffdi_218_fd_fie_ix", "usgdp"]),
        (1, ["usgdp", "imffdi_218_fd_fie_ix", "usgdp"]),
    ],
)
def test_1(data: Tuple[int, List[str]], web: WebApi, com: ComApi, test_metadata: Any) -> None:
    nth, series_names = data
    for web_r, com_r in zip(web.get_nth_release(nth, series_names), com.get_nth_release(nth, series_names)):
        test_metadata(web_r, com_r)
        assert com_r.values_metadata == web_r.values_metadata
        assert com_r == web_r


@pytest.mark.parametrize(
    "data",
    [
        (-1, ["usgdp"]),
        (0, ["usgdp"]),
        (1, ["usgdp"]),
        (99999, ["usgdp"]),
        (-1, ["imffdi_218_fd_fie_ix"]),
        (0, ["imffdi_218_fd_fie_ix"]),
        (1, ["imffdi_218_fd_fie_ix"]),
        (-1, ["usgdp", "imffdi_218_fd_fie_ix"]),
        (0, ["usgdp", "imffdi_218_fd_fie_ix"]),
        (1, ["usgdp", "imffdi_218_fd_fie_ix"]),
        (-1, ["usgdp", "imffdi_218_fd_fie_ix", "usgdp"]),
        (0, ["usgdp", "imffdi_218_fd_fie_ix", "usgdp"]),
        (1, ["usgdp", "imffdi_218_fd_fie_ix", "usgdp"]),
    ],
)
def test_2(data: Tuple[int, List[str]], web: WebApi, com: ComApi, test_metadata: Any) -> None:
    nth, series_names = data
    for web_r, com_r in zip(
        web.get_nth_release(nth, series_names, include_times_of_change=True),
        com.get_nth_release(nth, series_names, include_times_of_change=True),
    ):
        test_metadata(web_r, com_r)
        assert com_r.values_metadata == web_r.values_metadata
        assert com_r == web_r


def test_error_1(web: WebApi, com: ComApi) -> None:
    nth = 1
    series_names: List[str] = []
    text = "No series names"

    with pytest.raises(ValueError, match=text):
        web.get_nth_release(nth, series_names)

    with pytest.raises(ValueError, match=text):
        com.get_nth_release(nth, series_names)


def test_error_2(web: WebApi, com: ComApi) -> None:
    nth = 1
    series_names: List[str] = []
    text = "No series names"

    with pytest.raises(ValueError, match=text):
        web.get_nth_release(nth, series_names, include_times_of_change=True)

    with pytest.raises(ValueError, match=text):
        com.get_nth_release(nth, series_names, include_times_of_change=True)


def test_error_3(web: WebApi, com: ComApi) -> None:
    nth = 1
    series_names = ["usgdp", "bad name"]
    text = "failed to retrieve:\n\tbad name error_message: Not found"

    with pytest.raises(GetEntitiesError, match=text) as error_1:
        web.get_nth_release(nth, series_names, raise_error=True)

    with pytest.raises(GetEntitiesError, match=text) as error_2:
        com.get_nth_release(nth, series_names, raise_error=True)

    assert error_1.value == error_2.value
