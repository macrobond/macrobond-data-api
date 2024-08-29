from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..conftest import MockAdapterBuilder


class TestWebOAuth2Session:
    def test_1(self, get_mock_adapter_builder: "MockAdapterBuilder") -> None:
        _, webApi = (
            get_mock_adapter_builder.add_discovery()
            .add_token(get_mock_adapter_builder.test_token_1)
            .add_series_response("usgdp")
        ).build()

        webApi.session.fetch_token()

        response = webApi.get_one_series("usgdp")

        assert response.name == "usgdp"

    def test_2(self, get_mock_adapter_builder: "MockAdapterBuilder") -> None:
        _, webApi = (
            get_mock_adapter_builder.add_discovery()
            .add_token(get_mock_adapter_builder.test_token_1)
            .add_series_response("usgdp")
        ).build()

        response = webApi.get_one_series("usgdp")

        assert response.name == "usgdp"

    def test_3(self, get_mock_adapter_builder: "MockAdapterBuilder") -> None:
        _, webApi = (
            get_mock_adapter_builder.add_discovery()
            .add_token(get_mock_adapter_builder.test_token_3, 0)
            .add_series_response("usgdp")
            .add_response("https://api.macrobondfinancial.com/v1/series/fetchseries?n=usgdp_1", 401, 0)
            .add_token(get_mock_adapter_builder.test_token_3, 0)
            .add_series_response("usgdp_1")
        ).build()

        webApi.session.fetch_token()

        response = webApi.get_one_series("usgdp")

        token_auth = webApi.session.auth2_session.token_auth

        assert response.name == "usgdp"

        response = webApi.get_one_series("usgdp_1")

        assert response.name == "usgdp_1"

    def test_4(self, get_mock_adapter_builder: "MockAdapterBuilder") -> None:
        _, webApi = (
            get_mock_adapter_builder.add_discovery()
            .add_token(get_mock_adapter_builder.test_token_1)
            .add_series_response("usgdp")
            .add_response("https://api.macrobondfinancial.com/v1/series/fetchseries?n=usgdp_1", 401, 0)
            .add_token(get_mock_adapter_builder.test_token_2)
            .add_series_response("usgdp_1")
        ).build()

        response = webApi.get_one_series("usgdp")

        assert response.name == "usgdp"

        response = webApi.get_one_series("usgdp_1")

        assert response.name == "usgdp_1"

    def test_5(self, get_mock_adapter_builder: "MockAdapterBuilder") -> None:
        _, webApi = (
            get_mock_adapter_builder.add_discovery()
            .add_token(get_mock_adapter_builder.test_token_3, 0)
            .add_series_response("usgdp")
            .add_response("https://api.macrobondfinancial.com/v1/series/fetchseries?n=usgdp_1", 401, 0)
            .add_token(get_mock_adapter_builder.test_token_3)
            .add_series_response("usgdp_1")
        ).build()

        webApi.session.fetch_token()

        token_auth = webApi.session.auth2_session.token_auth

        response = webApi.get_one_series("usgdp")
        assert response.name == "usgdp"

        token_auth = webApi.session.auth2_session.token_auth

        response = webApi.get_one_series("usgdp_1")

        assert response.name == "usgdp_1"
