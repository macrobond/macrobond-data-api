import pytest

from macrobond_data_api.web import WebApi


@pytest.mark.parametrize(
    "name",
    ["rel_uspricecpi", "rel_usbeana"],
)
def test_web_get_upcomingreleases(name: str, web: WebApi) -> None:
    actual = web.session.release.get_upcomingreleases(name)

    assert len(actual) == 1

    assert actual[0]["events"]
    assert len(actual[0]["events"]) != 0

    assert actual[0]["metadata"]
    assert len(actual[0]["metadata"]) != 0

    assert actual[0]["metadata"]["Name"] == name
    assert actual[0]["metadata"]["PrimName"] == name
