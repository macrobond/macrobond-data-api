import pytest

from macrobond_data_api.web import AuthDiscoveryException, AuthFetchTokenException, AuthInvalidCredentialsException
from ..mock_adapter_builder import MAB, discovery_url, token_endpoint


@pytest.mark.no_account
class TestAuthClientDiscovery:

    def test(self, mab: MAB) -> None:
        _, _, _, auth_client = (mab.discovery()).build()

        auth_client._discovery(auth_client.authorization_url)

    def test_error_status_code(self, mab: MAB) -> None:
        _, _, session, _ = (mab.response(discovery_url, 500)).build()

        with pytest.raises(AuthDiscoveryException, match="status code is not 200"):
            session.get("")

    def test_error_not_valid_json(self, mab: MAB) -> None:
        _, _, session, _ = (mab.response(discovery_url, 200, "Boom!")).build()

        with pytest.raises(AuthDiscoveryException, match="not valid json"):
            session.get("")

    def test_error_no_root_obj(self, mab: MAB) -> None:
        _, _, session, _ = (mab.response(discovery_url, 200, '""')).build()

        with pytest.raises(AuthDiscoveryException, match="no root obj in json"):
            session.get("")

    def test_error_token_endpoint_in_root_obj(self, mab: MAB) -> None:
        _, _, session, _ = (mab.response(discovery_url, 200, {})).build()

        with pytest.raises(AuthDiscoveryException, match="token_endpoint in root obj"):
            session.get("")


@pytest.mark.no_account
class TestAuthClientFetchToken:

    def test_expires_at(self, mab: MAB) -> None:
        _, _, _, auth_client = (
            mab.response(token_endpoint, 200, {"token_type": "Bearer", "expires_at": 10, "access_token": "test"})
        ).build()

        auth_client._fetch_token(token_endpoint)
        assert auth_client.expires_at == 10

    def test_expires_in(self, mab: MAB) -> None:
        _, _, _, auth_client = (
            (mab.response(token_endpoint, 200, {"token_type": "Bearer", "expires_in": 10, "access_token": "test"}))
            .set_fetch_token_get_time([10])
            .build()
        )

        auth_client._fetch_token(token_endpoint)
        assert auth_client.expires_at == 20

    def test_error_status_code(self, mab: MAB) -> None:
        _, _, session, _ = (mab.discovery().response(token_endpoint, 500)).build()

        with pytest.raises(AuthFetchTokenException, match="status code is not 200 or 400"):
            session.get("")

    def test_error_not_valid_json(self, mab: MAB) -> None:
        _, _, session, _ = (mab.discovery().response(token_endpoint, 200, "Boom!")).build()

        with pytest.raises(AuthFetchTokenException, match="not valid json"):
            session.get("")

    def test_error_no_root_obj(self, mab: MAB) -> None:
        _, _, session, _ = (mab.discovery().response(token_endpoint, 200, '""')).build()

        with pytest.raises(AuthFetchTokenException, match="no root obj in json"):
            session.get("")

    def test_error_invalid_client_credentials(self, mab: MAB) -> None:
        _, _, session, _ = (mab.discovery().response(token_endpoint, 400, {"error": "invalid_client"})).build()

        with pytest.raises(AuthInvalidCredentialsException, match="invalid client credentials"):
            session.get("")

    def test_error_400_error(self, mab: MAB) -> None:
        _, _, session, _ = (mab.discovery().response(token_endpoint, 400, {"error": "test error"})).build()

        with pytest.raises(AuthFetchTokenException, match="error: test error"):
            session.get("")

    def test_error_400_no_error_in_response(self, mab: MAB) -> None:
        _, _, session, _ = (mab.discovery().response(token_endpoint, 400, {})).build()

        with pytest.raises(AuthFetchTokenException, match="no error in response"):
            session.get("")

    def test_error_200_token_type(self, mab: MAB) -> None:
        _, _, session, _ = (mab.discovery().response(token_endpoint, 200, {"token_type": "test"})).build()

        with pytest.raises(AuthFetchTokenException, match="token_type is not Bearer"):
            session.get("")

    def test_error_200_no_expires_at_or_expires_in_in_response(self, mab: MAB) -> None:
        _, _, session, _ = (mab.discovery().response(token_endpoint, 200, {"token_type": "Bearer"})).build()

        with pytest.raises(AuthFetchTokenException, match="no expires_at or expires_in"):
            session.get("")

    def test_error_200_no_access_token(self, mab: MAB) -> None:
        _, _, session, _ = (
            mab.discovery().response(token_endpoint, 200, {"token_type": "Bearer", "expires_at": 1})
        ).build()

        with pytest.raises(AuthFetchTokenException, match="No access_token"):
            session.get("")


@pytest.mark.no_account
class TestAuthClient:

    def test_fetch_token_1(self, mab: MAB) -> None:
        _, _, _, auth_client = (mab.auth()).build()

        auth_client.fetch_token()

    def test_fetch_token_if_necessary_1(self, mab: MAB) -> None:
        _, _, _, auth_client = (mab.auth()).build()

        auth_client.fetch_token_if_necessary()

    def test_fetch_token_if_necessary_2(self, mab: MAB) -> None:
        _, _, _, auth_client = (mab.auth()).build()

        auth_client.fetch_token_if_necessary()

        auth_client.fetch_token_if_necessary()

    def test_fetch_token_if_necessary_3(self, mab: MAB) -> None:
        _, _, _, auth_client = mab.set_no_assert().build()
        assert auth_client.is_expired_get_time() == 0
        assert auth_client.is_expired_get_time() == 0

        assert auth_client.fetch_token_get_time() == 0
        assert auth_client.fetch_token_get_time() == 0

    def test_fetch_token_if_necessary_4(self, mab: MAB) -> None:
        mock_adapter, _, _, auth_client = (mab.auth(10).token().set_is_expired_get_time([0, 11, 11])).build()

        assert auth_client.fetch_token_if_necessary() is True
        assert mock_adapter.index == 2

        assert auth_client.fetch_token_if_necessary() is False
        assert mock_adapter.index == 2

        assert auth_client.fetch_token_if_necessary() is True
        assert mock_adapter.index == 3

        assert auth_client.fetch_token_if_necessary() is False
        assert mock_adapter.index == 3

    def test_leeway_1(self, mab: MAB) -> None:
        mock_adapter, _, _, auth_client = (
            mab.auth(10).token().set_is_expired_get_time([0, 10, 10]).set_leeway(1)
        ).build()

        assert auth_client.fetch_token_if_necessary() is True
        assert mock_adapter.index == 2

        assert auth_client.fetch_token_if_necessary() is False
        assert mock_adapter.index == 2

        assert auth_client.fetch_token_if_necessary() is True
        assert mock_adapter.index == 3

        assert auth_client.fetch_token_if_necessary() is False
        assert mock_adapter.index == 3
