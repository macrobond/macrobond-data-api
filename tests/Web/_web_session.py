# -*- coding: utf-8 -*-

from typing import Any

from unittest import TestCase  # type: ignore
from unittest.mock import Mock

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


class WebSession(TestCase):
    def test_get_200(self) -> None:
        mock = Mock()
        session = Session(
            "",
            "",
            api_url="https://",
            authorization_url="https://",
            test_auth2_session=mock,
        )

        mock.get.return_value = new_response(200)

        response = session.get("")

        # asserts

        self.assertEqual(response.status_code, 200)

        mock.get.assert_called_with(
            url="https://",
            params=None,
            stream=False,
            proxies=None,
            headers={"Accept": "application/json; charset=utf-8"},
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

        mock.get.side_effect = [new_response(401), new_response(200)]
        mock.request.return_value = new_response(200, {"token_endpoint": ""})

        response = session.get("")

        # asserts

        self.assertEqual(response.status_code, 200)

        mock.get.assert_called_with(
            url="https://",
            params=None,
            stream=False,
            proxies=None,
            headers={"Accept": "application/json; charset=utf-8"},
        )
        mock.request.assert_called_with(
            "get",
            "https://.well-known/openid-configuration",
            True,
            proxies=None,
        )
        mock.fetch_token.assert_called_with("", proxies=None)

    def test_discovery_error_status_code(self) -> None:
        mock = Mock()
        session = Session(
            "", "", api_url="https://", authorization_url="https://", test_auth2_session=mock
        )

        mock.get.return_value = new_response(401)
        mock.request.return_value = new_response(500)

        with self.assertRaises(Exception) as context_manager:
            session.get("")
        ex = context_manager.exception

        # asserts

        self.assertEqual(ex.args[0], "discovery Exception, status code is not 200")

        mock.get.assert_called_with(
            url="https://",
            params=None,
            stream=False,
            proxies=None,
            headers={"Accept": "application/json; charset=utf-8"},
        )

        mock.request.assert_called_with(
            "get", "https://.well-known/openid-configuration", True, proxies=None
        )

    def test_discovery_error_not_valid_json(self) -> None:
        mock = Mock()
        session = Session(
            "", "", api_url="https://", authorization_url="https://", test_auth2_session=mock
        )

        mock.get.return_value = new_response(401)
        mock.request.return_value = new_response(200, side_effect=Exception("Boom!"))

        with self.assertRaises(Exception) as context_manager:
            session.get("")
        ex = context_manager.exception

        # asserts

        self.assertEqual(ex.args[0], "discovery Exception, not valid json.")

        mock.get.assert_called_with(
            url="https://",
            params=None,
            stream=False,
            proxies=None,
            headers={"Accept": "application/json; charset=utf-8"},
        )

        mock.request.assert_called_with(
            "get", "https://.well-known/openid-configuration", True, proxies=None
        )

    def test_discovery_error_no_root_obj(self) -> None:
        mock = Mock()
        session = Session(
            "", "", api_url="https://", authorization_url="https://", test_auth2_session=mock
        )

        mock.get.return_value = new_response(401)
        mock.request.return_value = new_response(200, json="")

        with self.assertRaises(Exception) as context_manager:
            session.get("")
        ex = context_manager.exception

        # asserts

        self.assertEqual(ex.args[0], "discovery Exception, no root obj in json.")

        mock.get.assert_called_with(
            url="https://",
            params=None,
            stream=False,
            proxies=None,
            headers={"Accept": "application/json; charset=utf-8"},
        )

        mock.request.assert_called_with(
            "get", "https://.well-known/openid-configuration", True, proxies=None
        )

    def test_discovery_error_token_endpoint_in_root_obj(self) -> None:
        mock = Mock()
        session = Session(
            "", "", api_url="https://", authorization_url="https://", test_auth2_session=mock
        )

        mock.get.return_value = new_response(401)
        mock.request.return_value = new_response(200, json={})

        with self.assertRaises(Exception) as context_manager:
            session.get("")
        ex = context_manager.exception

        # asserts

        self.assertEqual(ex.args[0], "discovery Exception, token_endpoint in root obj.")

        mock.get.assert_called_with(
            url="https://",
            params=None,
            stream=False,
            proxies=None,
            headers={"Accept": "application/json; charset=utf-8"},
        )

        mock.request.assert_called_with(
            "get", "https://.well-known/openid-configuration", True, proxies=None
        )
