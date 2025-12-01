from typing import List, Tuple, Union, Any, Dict, Optional
from io import BytesIO

from json import dumps as json_dump
from unittest.mock import Mock

from requests import Response
from requests.models import Response as ResponseModel

from macrobond_data_api.web.session import Session
from macrobond_data_api.web._auth_client import _AuthClient
from macrobond_data_api.web._access_token_cache import _AccessTokenCache
from macrobond_data_api.web import WebApi

from .mock_adapter import MockAdapter

API_URL = "https://api/"
AUTHORIZATION_URL = "https://auth/"
DISCOVERY_URL = "https://auth/.well-known/openid-configuration"
TOKEN_ENDPOINT = "https://auth/get_a_nice_token"


class MockAdapterBuilder:

    def __init__(self) -> None:
        self._urls: List[str] = []
        self._responses: List[Response] = []
        self._access_token_index = 1
        self._leeway = 0
        self._fetch_token_get_time: Optional[List[int]] = None
        self._is_expired_get_time: Optional[List[int]] = None
        self._remove_old_cache_items_time: Optional[List[int]] = None
        self._mock_adapter: Optional[MockAdapter] = None
        self._no_assert = False
        self._use_access_token_cache = False

    def build(self) -> Tuple[MockAdapter, WebApi, Session, _AuthClient]:

        _AccessTokenCache._cache.clear()

        session = Session(
            "",
            "",
            api_url=API_URL,
            authorization_url=AUTHORIZATION_URL,
            use_access_token_cache=self._use_access_token_cache,
        )

        self._mock_adapter = mock_adapter = MockAdapter(self._responses, self._urls)
        session.requests_session.mount("https://", mock_adapter)
        auth_client = session._auth_client
        auth_client.leeway = self._leeway

        mock = Mock()
        if self._fetch_token_get_time:
            mock.fetch_token_get_time.side_effect = self._fetch_token_get_time
            auth_client.fetch_token_get_time = mock.fetch_token_get_time
        else:
            auth_client.fetch_token_get_time = lambda: 0

        if self._is_expired_get_time:
            mock.is_expired_get_time.side_effect = self._is_expired_get_time
            auth_client.is_expired_get_time = mock.is_expired_get_time
        else:
            auth_client.is_expired_get_time = lambda: 0

        return mock_adapter, WebApi(session), session, auth_client

    def use_access_token_cache(self) -> "MockAdapterBuilder":
        self._use_access_token_cache = True
        return self

    def set_no_assert(self) -> "MockAdapterBuilder":
        self._no_assert = True
        return self

    def set_leeway(self, leeway: int) -> "MockAdapterBuilder":
        self._leeway = leeway
        return self

    def set_fetch_token_get_time(self, fetch_token_get_time: List[int]) -> "MockAdapterBuilder":
        self._fetch_token_get_time = fetch_token_get_time
        return self

    def set_is_expired_get_time(self, is_expired_get_time: List[int]) -> "MockAdapterBuilder":
        self._is_expired_get_time = is_expired_get_time
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

        self._responses.append(response)
        self._urls.append(url)

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
            DISCOVERY_URL,
            200,
            {
                "token_endpoint": TOKEN_ENDPOINT,
            },
        )

    def token(self, expires_in: int = None) -> "MockAdapterBuilder":
        if expires_in is None:
            expires_in = 3600

        name = "Test Token " + str(self._access_token_index)
        self._access_token_index += 1

        return self.response(
            TOKEN_ENDPOINT,
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
        if self._no_assert:
            return

        assert self._mock_adapter
        self._mock_adapter.assert_this()


MAB = MockAdapterBuilder
