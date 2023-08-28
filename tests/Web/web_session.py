from typing import Any

from unittest.mock import Mock, call

import pytest

from macrobond_data_api.web.session import Session

# TODO @mb-jp add tests using proxie


def new_response(status_code: int, json: Any = None, side_effect: Any = None) -> Mock:
    response = Mock()
    response.status_code = status_code
    if json is not None:
        response.json.return_value = json
    if side_effect is not None:
        response.json.side_effect = side_effect
    return response


class TestWebSession:
    def test_get_200(self) -> None:
        mock = Mock()
        session = Session(
            "",
            "",
            api_url="https://",
            authorization_url="https://",
            test_auth2_session=mock,
        )

        mock.request.return_value = new_response(200)

        # test

        response = session.get("")

        # asserts

        assert response.status_code == 200

        mock.request.assert_called_with(
            "GET",
            "https://",
            params=None,
            json=None,
            stream=False,
            proxies=None,
            headers={"Accept": "application/json"},
        )

    def test_retry(self) -> None:
        mock = Mock()
        session = Session(
            "",
            "",
            api_url="https://",
            authorization_url="https://",
            test_auth2_session=mock,
        )

        mock.request.side_effect = [new_response(401), new_response(200, {"token_endpoint": ""}), new_response(200)]

        # test

        response = session.get("")

        # asserts

        assert response.status_code == 200

        mock.request.assert_has_calls(
            [
                call(
                    "GET",
                    "https://",
                    params=None,
                    json=None,
                    stream=False,
                    proxies=None,
                    headers={"Accept": "application/json"},
                ),
                call(
                    "GET",
                    "https://.well-known/openid-configuration",
                    True,
                    proxies=None,
                ),
                call(
                    "GET",
                    "https://",
                    params=None,
                    json=None,
                    stream=False,
                    proxies=None,
                    headers={"Accept": "application/json"},
                ),
            ]
        )

        mock.fetch_token.assert_called_with("", proxies=None)

    def test_discovery_error_status_code(self) -> None:
        mock = Mock()
        session = Session("", "", api_url="https://", authorization_url="https://", test_auth2_session=mock)

        mock.request.side_effect = [new_response(401), new_response(500)]

        # test

        with pytest.raises(Exception, match="discovery Exception, status code is not 200"):
            session.get("")

        # asserts

        mock.request.assert_has_calls(
            [
                call(
                    "GET",
                    "https://",
                    params=None,
                    json=None,
                    stream=False,
                    proxies=None,
                    headers={"Accept": "application/json"},
                ),
                call("GET", "https://.well-known/openid-configuration", True, proxies=None),
            ]
        )

    def test_discovery_error_not_valid_json(self) -> None:
        mock = Mock()
        session = Session("", "", api_url="https://", authorization_url="https://", test_auth2_session=mock)

        mock.request.side_effect = [new_response(401), new_response(200, side_effect=Exception("Boom!"))]

        # test

        with pytest.raises(Exception, match="discovery Exception, not valid json."):
            session.get("")

        # asserts

        mock.request.assert_has_calls(
            [
                call(
                    "GET",
                    "https://",
                    params=None,
                    json=None,
                    stream=False,
                    proxies=None,
                    headers={"Accept": "application/json"},
                ),
                call("GET", "https://.well-known/openid-configuration", True, proxies=None),
            ]
        )

    def test_discovery_error_no_root_obj(self) -> None:
        mock = Mock()
        session = Session("", "", api_url="https://", authorization_url="https://", test_auth2_session=mock)

        mock.request.side_effect = [new_response(401), new_response(200, json="")]

        # test

        with pytest.raises(Exception, match="discovery Exception, no root obj in json."):
            session.get("")

        # asserts

        mock.request.assert_has_calls(
            [
                call(
                    "GET",
                    "https://",
                    params=None,
                    json=None,
                    stream=False,
                    proxies=None,
                    headers={"Accept": "application/json"},
                ),
                call("GET", "https://.well-known/openid-configuration", True, proxies=None),
            ]
        )

    def test_discovery_error_token_endpoint_in_root_obj(self) -> None:
        mock = Mock()
        session = Session("", "", api_url="https://", authorization_url="https://", test_auth2_session=mock)

        mock.request.side_effect = [new_response(401), new_response(200, json={})]

        # test

        with pytest.raises(Exception, match="discovery Exception, token_endpoint in root obj."):
            session.get("")

        # asserts

        mock.request.assert_has_calls(
            [
                call(
                    "GET",
                    "https://",
                    params=None,
                    json=None,
                    stream=False,
                    proxies=None,
                    headers={"Accept": "application/json"},
                ),
                call("GET", "https://.well-known/openid-configuration", True, proxies=None),
            ]
        )
