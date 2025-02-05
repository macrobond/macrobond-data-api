from datetime import datetime
import pytest

from macrobond_data_api.web import WebApi


@pytest.mark.parametrize(
    "name",
    ["rel_uspricecpi", "rel_usbeana"],
)
def test_upcomingreleases_1(name: str, web: WebApi) -> None:
    actual = web.upcoming_releases([name])

    assert len(actual) == 1

    assert actual[0].events
    assert len(actual[0].events) != 0

    assert actual[0].metadata
    assert len(actual[0].metadata) != 0

    assert actual[0].name == name
    assert actual[0].primary_name == name


def test_upcomingreleases_2(web: WebApi) -> None:
    actual = web.upcoming_releases(["rel_usbeana", "a bade name"])

    assert len(actual) == 2

    assert actual[0].events
    assert len(actual[0].events) != 0

    assert actual[0].metadata
    assert len(actual[0].metadata) != 0

    assert actual[0].name == "rel_usbeana"
    assert actual[0].primary_name == "rel_usbeana"

    assert actual[1].is_error
    assert actual[1].error_message
    assert actual[1].events is None
    assert actual[1].metadata is None


# not working for now
# def test_upcomingreleases_3(web: WebApi) -> None:
#     with pytest.raises(Exception) as ex:
#         web.upcoming_releases(["rel_usbeana", "a bade name"], raise_error=True)
#


def test_upcomingreleases_4(web: WebApi) -> None:
    actual = web.upcoming_releases(["rel_usbeana"], end_time=datetime(2000, 2, 3, 4, 5, 6))

    assert actual[0].events is not None
    assert len(actual[0].events) == 0
