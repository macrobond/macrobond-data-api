# -*- coding: utf-8 -*-

from typing import Callable, Dict, Optional, Any, TYPE_CHECKING, Sequence

from authlib.integrations.requests_client import OAuth2Session  # type: ignore
from authlib.integrations.base_client.errors import InvalidTokenError  # type: ignore
from .web_types import (
    MetadataMethods,
    SearchMethods,
    SeriesMethods,
    SeriesTreeMethods,
    HttpException,
    ProblemDetailsException,
)

from .scope import Scope
from ._metadata_directory import _MetadataTypeDirectory
from ._metadata import _Metadata

_socks_import_error: Optional[ImportError] = None
try:
    import socks as _  # type: ignore
except ImportError as ex:
    _socks_import_error = ex

API_URL_DEFAULT = "https://api.macrobondfinancial.com/"
AUTHORIZATION_URL_DEFAULT = "https://apiauth.macrobondfinancial.com/mbauth/"

if TYPE_CHECKING:  # pragma: no cover
    from requests import Response  # type: ignore

__pdoc__ = {
    "Session.__init__": False,
}


def _raise_on_error(response: "Response", non_error_status: Sequence[int] = None) -> None:
    if non_error_status is None:
        non_error_status = [200]

    if response.status_code in non_error_status:
        return

    content_type = response.headers.get("Content-Type")
    if ["application/json; charset=utf-8", "application/json"].count(content_type) != 0:
        raise ProblemDetailsException.create_from_response(response)

    macrobond_status = response.headers.get("X-Macrobond-Status")
    if macrobond_status:
        raise ProblemDetailsException(response, detail=macrobond_status)

    raise HttpException(response)


class Session:
    @property
    def metadata(self) -> MetadataMethods:
        """Metadata operations"""
        return self.__metadata

    @property
    def search(self) -> SearchMethods:
        """Search for time series and other entites"""
        return self.__search

    @property
    def series(self) -> SeriesMethods:
        """Time series and entity operations"""
        return self.__series

    @property
    def series_tree(self) -> SeriesTreeMethods:
        """Operations related to the visual series database tree structure"""
        return self.__series_tree

    @property
    def api_url(self):
        return self.__api_url

    @property
    def authorization_url(self):
        return self.__authorization_url

    @property
    def token_endpoint(self):
        return self.__token_endpoint

    @property
    def auth2_session(self):
        return self.__auth2_session

    def __init__(
        self,
        username: str,
        password: str,
        *scopes: Scope,
        api_url: str = API_URL_DEFAULT,
        authorization_url: str = API_URL_DEFAULT,
        proxy: str = None,
        test_auth2_session: Any = None
    ) -> None:

        self.__proxies: Optional[Dict[str, str]] = None
        if proxy:
            if proxy.lower().startswith("socks5://") and _socks_import_error:
                raise _socks_import_error
            self.__proxies = {"https": proxy, "http": proxy}

        self.__token_endpoint: Optional[str] = None

        if not authorization_url.lower().startswith("https://"):
            raise ValueError("authorization_url is not https")

        if not api_url.lower().startswith("https://"):
            raise ValueError("api_url is not https")

        if not authorization_url.endswith("/"):
            authorization_url = authorization_url + "/"
        self.__authorization_url = authorization_url

        if not api_url.endswith("/"):
            api_url = api_url + "/"
        self.__api_url = api_url

        scopes_str_list = list(map(lambda s: s.value, scopes))
        if test_auth2_session is None:
            self.__auth2_session = OAuth2Session(username, password, scope=scopes_str_list)
        else:
            self.__auth2_session = test_auth2_session

        self.__metadata = MetadataMethods(self)
        self.__search = SearchMethods(self)
        self.__series = SeriesMethods(self)
        self.__series_tree = SeriesTreeMethods(self)

        self._metadata_type_directory = _MetadataTypeDirectory(self)

    def close(self) -> None:
        self.auth2_session.close()
        self._metadata_type_directory.close()

    def fetch_token(self) -> None:
        if self.token_endpoint is None:
            self.__token_endpoint = self.discovery(self.authorization_url)
        self.auth2_session.fetch_token(self.token_endpoint, proxies=self.__proxies)

    def get(self, url: str, params: dict = None, stream=False) -> "Response":
        def http():
            return self.auth2_session.get(
                url=self.api_url + url, params=params, stream=stream, proxies=self.__proxies
            )

        return self.__if_status_code_401_fetch_token_and_retry(http)

    def get_or_raise(
        self, url: str, params: dict = None, non_error_status: Sequence[int] = None, stream=False
    ) -> "Response":
        response = self.get(url, params, stream=stream)
        _raise_on_error(response, non_error_status)
        return response

    def post(self, url: str, params: dict = None, json: object = None, stream=False) -> "Response":
        def http():
            return self.auth2_session.post(
                url=self.api_url + url,
                params=params,
                json=json,
                stream=stream,
                proxies=self.__proxies,
            )

        return self.__if_status_code_401_fetch_token_and_retry(http)

    def post_or_raise(
        self,
        url: str,
        params: dict = None,
        json: object = None,
        non_error_status: Sequence[int] = None,
        stream=False,
    ) -> "Response":
        response = self.post(url, params, json, stream=stream)
        _raise_on_error(response, non_error_status)
        return response

    def discovery(self, url: str) -> str:
        response = self.auth2_session.request(
            "get", url + ".well-known/openid-configuration", True, proxies=self.__proxies
        )
        if response.status_code != 200:
            raise Exception("discovery Exception, status code is not 200")

        try:
            json: Optional[dict] = response.json()
        except BaseException as base_exception:
            raise Exception("discovery Exception, not valid json.") from base_exception

        if not isinstance(json, dict):
            raise Exception("discovery Exception, no root obj in json.")

        token_endpoint: Optional[str] = json.get("token_endpoint")
        if token_endpoint is None:
            raise Exception("discovery Exception, token_endpoint in root obj.")

        return token_endpoint

    def __if_status_code_401_fetch_token_and_retry(
        self, http: Callable[[], "Response"]
    ) -> "Response":
        try:
            response = http()
        except InvalidTokenError:
            self.fetch_token()
            return http()
        if response.status_code == 401:
            self.fetch_token()
            response = http()
        return response

    def _create_metadata(self, metadata: dict) -> _Metadata:
        return _Metadata(metadata, self._metadata_type_directory)
