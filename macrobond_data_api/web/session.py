from typing import Callable, Dict, Optional, Any, TYPE_CHECKING, Sequence, cast

from authlib.integrations.requests_client import OAuth2Session
from authlib.integrations.base_client.errors import InvalidTokenError
from macrobond_data_api.common.types import Metadata

from .web_types import (
    MetadataMethods,
    SearchMethods,
    SeriesMethods,
    SeriesTreeMethods,
    InHouseSeriesMethods,
    HttpException,
    ProblemDetailsException,
)

from .scope import Scope
from ._metadata_directory import _MetadataTypeDirectory
from ._metadata import _Metadata

_socks_import_error: Optional[ImportError] = None
try:
    import socks as _
except ImportError as ex:
    _socks_import_error = ex

API_URL_DEFAULT = "https://api.macrobondfinancial.com/"
AUTHORIZATION_URL_DEFAULT = "https://apiauth.macrobondfinancial.com/mbauth/"

if TYPE_CHECKING:  # pragma: no cover
    from requests import Response

__pdoc__ = {
    "Session.__init__": False,
}


class _ResponseAsFileObject:
    def __init__(self, response: "Response", chunk_size: int = 65536) -> None:
        self.data = response.iter_content(chunk_size=chunk_size)

    def read(self, n: int) -> bytes:
        if n == 0:
            return b""
        return next(self.data, b"")


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
    def in_house_series(self) -> InHouseSeriesMethods:
        """Additional operations for in-house series"""
        return self.__in_house_series

    @property
    def api_url(self) -> str:
        return self.__api_url

    @property
    def authorization_url(self) -> str:
        return self.__authorization_url

    @property
    def token_endpoint(self) -> Optional[str]:
        return self.__token_endpoint

    @property
    def auth2_session(self) -> OAuth2Session:
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

        if not self._is_https_url(authorization_url):
            raise ValueError("authorization_url is not https")

        if not self._is_https_url(api_url):
            raise ValueError("api_url is not https")

        if not authorization_url.endswith("/"):
            authorization_url = authorization_url + "/"
        self.__authorization_url = authorization_url

        if not api_url.endswith("/"):
            api_url = api_url + "/"
        self.__api_url = api_url

        if test_auth2_session is None:
            self.__auth2_session = OAuth2Session(username, password, scope=[x.value for x in scopes])
        else:
            self.__auth2_session = test_auth2_session

        self.__metadata = MetadataMethods(self)
        self.__search = SearchMethods(self)
        self.__series = SeriesMethods(self)
        self.__series_tree = SeriesTreeMethods(self)
        self.__in_house_series = InHouseSeriesMethods(self)

        self._metadata_type_directory = _MetadataTypeDirectory(self)

        self._is_open = True

    def _is_https_url(self, url: str) -> bool:
        return url.lower().startswith("https://")

    def close(self) -> None:
        if not self._is_open:
            return
        self.auth2_session.close()
        self._metadata_type_directory.close()
        self._is_open = False

    def fetch_token(self) -> None:
        if not self._is_open:
            raise ValueError("Session is not open")

        if self.token_endpoint is None:
            self.__token_endpoint = self.discovery(self.authorization_url)
        self.auth2_session.fetch_token(self.token_endpoint, proxies=self.__proxies)

    def get(self, url: str, params: dict = None, stream: bool = False) -> "Response":
        return self._request("GET", url, params, None, stream)

    def get_or_raise(
        self,
        url: str,
        params: dict = None,
        non_error_status: Sequence[int] = None,
        stream: bool = False,
    ) -> "Response":
        return self.raise_on_error(self.get(url, params, stream=stream), non_error_status)

    def post(self, url: str, params: dict = None, json: object = None, stream: bool = False) -> "Response":
        return self._request("POST", url, params, json, stream)

    def post_or_raise(
        self,
        url: str,
        params: dict = None,
        json: object = None,
        non_error_status: Sequence[int] = None,
        stream: bool = False,
    ) -> "Response":
        return self.raise_on_error(self.post(url, params, json, stream=stream), non_error_status)

    def delete(self, url: str, params: dict = None, stream: bool = False) -> "Response":
        return self._request("DELETE", url, params, None, stream)

    def delete_or_raise(
        self,
        url: str,
        params: dict = None,
        non_error_status: Sequence[int] = None,
        stream: bool = False,
    ) -> "Response":
        return self.raise_on_error(self.delete(url, params, stream=stream), non_error_status)

    def raise_on_error(self, response: "Response", non_error_status: Sequence[int] = None) -> "Response":
        if non_error_status is None:
            non_error_status = [200]

        if response.status_code in non_error_status:
            return response

        content_type = response.headers.get("Content-Type")

        if content_type in ["application/json; charset=utf-8", "application/json"]:
            raise ProblemDetailsException.create_from_response(response)

        macrobond_status = response.headers.get("X-Macrobond-Status")
        if macrobond_status:
            raise ProblemDetailsException(response, detail=macrobond_status)

        raise HttpException(response)

    def _response_to_file_object(self, response: "Response") -> _ResponseAsFileObject:
        return _ResponseAsFileObject(response)

    def _request(self, method: str, url: str, params: Optional[dict], json: object, stream: bool) -> "Response":
        if not self._is_open:
            raise ValueError("Session is not open")

        def http() -> "Response":
            return self.auth2_session.request(
                method,
                self.api_url + url,
                params=params,
                json=json,
                stream=stream,
                proxies=self.__proxies,
                headers={"Accept": "application/json"},
            )

        return self._if_status_code_401_fetch_token_and_retry(http)

    def discovery(self, url: str) -> str:
        if not self._is_open:
            raise ValueError("Session is not open")

        response = self.auth2_session.request(
            "GET", url + ".well-known/openid-configuration", True, proxies=self.__proxies
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

    def _if_status_code_401_fetch_token_and_retry(self, http: Callable[[], "Response"]) -> "Response":
        try:
            response = http()
        except InvalidTokenError:
            self.fetch_token()
            return http()
        if response.status_code == 401:
            self.fetch_token()
            response = http()
        return response

    def _create_metadata(self, data: Optional[Dict[str, Any]]) -> Metadata:
        return cast(Metadata, _Metadata(data, self._metadata_type_directory)) if data else {}
