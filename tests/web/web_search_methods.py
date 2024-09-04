from macrobond_data_api.web import WebApi


def test_web_entities_for_display(web: WebApi) -> None:
    actual = web.session.search.entities_for_display(
        {
            "filters": [
                {
                    "text": "abc",
                }
            ],
            "attributesForDisplayFormat": ["Name", "Class"],
        }
    )

    assert len(actual["results"]) != 0, "len(actual['results'])"

    assert "Name" in actual["results"][0]
    assert "Title" in actual["results"][0]
    assert "Class" in actual["results"][0]


def test_web_filter_lists(web: WebApi) -> None:
    web.session.search.filter_lists("*")


def test_web_get_entities(web: WebApi) -> None:
    actual = web.session.search.get_entities(text="abc")

    assert len(actual["results"]) != 0, "len(actual['results'])"

    assert "Name" in actual["results"][0]
