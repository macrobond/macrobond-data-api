import pytest
from ..mock_adapter_builder import MAB

# TODO @mb-jp add tests using proxie


@pytest.mark.no_account
class TestWebSession:
    def test_get_200(self, mab: MAB) -> None:
        _, _, session, _ = (mab.auth().response("https://api/test", 200, "test")).build()

        response = session.get("test")

        assert response.status_code == 200
        assert response.text == "test"

    def test_retry(self, mab: MAB) -> None:
        _, _, session, _ = (
            mab.auth().response("https://api/test", 401).token().response("https://api/test", 200, "test")
        ).build()

        response = session.get("test")

        assert response.status_code == 200
        assert response.text == "test"
