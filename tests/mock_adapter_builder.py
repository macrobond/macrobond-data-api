from typing import List, Tuple, Union, Any, Dict, Optional
from io import BytesIO

from json import dumps as json_dump
from unittest.mock import Mock

from requests import Response
from requests.models import Response as ResponseModel

from macrobond_data_api.web.session import Session
from macrobond_data_api.web._auth_client import _AuthClient
from macrobond_data_api.web import WebApi

from .mock_adapter import MockAdapter

api_url = "https://api/"
authorization_url = "https://auth/"
discovery_url = "https://auth/.well-known/openid-configuration"
token_endpoint = "https://auth/get_a_nice_token"


class MockAdapterBuilder:

    def __init__(self) -> None:
        self.urls: List[str] = []
        self.responses: List[Response] = []
        self._access_token_index = 1
        self.leeway = 0
        self.fetch_token_get_time: Optional[List[int]] = None
        self.is_expired_get_time: Optional[List[int]] = None
        self._mockAdapter: Optional[MockAdapter] = None
        self.no_assert = False

    def build(self) -> Tuple[MockAdapter, WebApi, Session, _AuthClient]:
        session = Session("", "", api_url=api_url, authorization_url=authorization_url)

        self._mockAdapter = mock_adapter = MockAdapter(self.responses, self.urls)
        session.requests_session.mount("https://", mock_adapter)
        auth_client = session._auth_client
        auth_client.leeway = self.leeway

        mock = Mock()
        if self.fetch_token_get_time:
            mock.fetch_token_get_time.side_effect = self.fetch_token_get_time
            auth_client.fetch_token_get_time = mock.fetch_token_get_time
        else:
            auth_client.fetch_token_get_time = lambda: 0

        if self.is_expired_get_time:
            mock.is_expired_get_time.side_effect = self.is_expired_get_time
            auth_client.is_expired_get_time = mock.is_expired_get_time
        else:
            auth_client.is_expired_get_time = lambda: 0

        return mock_adapter, WebApi(session), session, auth_client

    def set_no_assert(self) -> "MockAdapterBuilder":
        self.no_assert = True
        return self

    def set_leeway(self, leeway: int) -> "MockAdapterBuilder":
        self.leeway = leeway
        return self

    def set_fetch_token_get_time(self, fetch_token_get_time: List[int]) -> "MockAdapterBuilder":
        self.fetch_token_get_time = fetch_token_get_time
        return self

    def set_is_expired_get_time(self, is_expired_get_time: List[int]) -> "MockAdapterBuilder":
        self.is_expired_get_time = is_expired_get_time
        return self

    def response(
        self,
        url: str,
        status_code: int,
        json: Union[None, str, Any] = None,
        raw: Union[None, str, Dict[Any, Any], bytes] = None,
    ) -> "MockAdapterBuilder":
        response = ResponseModel()
        response.status_code = status_code
        response.history = []

        if raw:
            if isinstance(raw, dict):
                raw = json_dump(raw)
            if isinstance(raw, str):
                raw = bytes(raw, "utf-8")
            response.raw = BytesIO(raw)
        else:
            if isinstance(json, str):
                response._content = json.encode()
            elif json is not None:
                response._content = json_dump(json).encode()

        self.responses.append(response)
        self.urls.append(url)

        return self

    def series_response(self, name: str, url: str = None, status_code: int = None) -> "MockAdapterBuilder":
        if url is None:
            url = f"https://api/v1/series/fetchseries?n={name}"
        if status_code is None:
            status_code = 200
        return self.response(
            url,
            status_code,
            [
                {
                    "dates": ["2021-01-01", "2021-01-02"],
                    "values": [1.0, 2.0],
                    "metadata": {"PrimName": name},
                }
            ],
        )

    def get_data_package_list(self, raw: Dict[Any, Any]) -> "MockAdapterBuilder":
        return self.response("https://api/v1/series/getdatapackagelist", 200, raw=raw)

    def auth(self, expires_in: int = None) -> "MockAdapterBuilder":
        return self.discovery().token(expires_in)

    def discovery(self) -> "MockAdapterBuilder":
        return self.response(
            discovery_url,
            200,
            {
                "token_endpoint": token_endpoint,
            },
        )

    def token(self, expires_in: int = None) -> "MockAdapterBuilder":
        if expires_in is None:
            expires_in = 3600

        name = "Test Token " + str(self._access_token_index)
        self._access_token_index += 1

        return self.response(
            token_endpoint,
            200,
            {
                "access_token": json_dump(
                    {
                        "name": name,
                        "exp": expires_in,
                    }
                ),
                "expires_in": expires_in,
                "token_type": "Bearer",
                "scope": "mb.test",
                "name": name,
            },
        )

    def assert_this(self) -> None:
        if self.no_assert:
            return

        assert self._mockAdapter
        self._mockAdapter.assert_this()


MAB = MockAdapterBuilder
