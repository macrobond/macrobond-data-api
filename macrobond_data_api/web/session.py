from typing import Dict, Optional, Any, TYPE_CHECKING, Sequence, Type, cast

from requests.sessions import Session as RequestsSession
from macrobond_data_api.common.types import Metadata
from macrobond_data_api.web._auth_client import _AuthClient

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
from .configuration import Configuration


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

    configuration: Type[Configuration] = Configuration

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
        return self._auth_client.authorization_url

    @property
    def token_endpoint(self) -> Optional[str]:
        return self._auth_client.token_endpoint

    def __init__(
        self,
        username: str,
        password: str,
        *scopes: Scope,
        api_url: str = None,
        authorization_url: str = None,
        proxy: str = None,
    ) -> None:
        if api_url is None:
            api_url = Configuration._default_api_url

        if authorization_url is None:
            authorization_url = Configuration._default_authorization_url

        if not self._is_https_url(authorization_url):
            raise ValueError("authorization_url is not https")

        if not self._is_https_url(api_url):
            raise ValueError("api_url is not https")

        if not authorization_url.endswith("/"):
            authorization_url = authorization_url + "/"

        if not api_url.endswith("/"):
            api_url = api_url + "/"
        self.__api_url = api_url

        self.requests_session = RequestsSession()
        if proxy:
            self.requests_session.proxies = {"https": proxy, "http": proxy}

        self._auth_client = _AuthClient(username, password, scopes, authorization_url, self)

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
        self.requests_session.close()
        self._metadata_type_directory.close()
        self._is_open = False

    def get(self, url: str, params: Dict[str, Any] = None, stream: bool = False) -> "Response":
        return self._request("GET", url, params, None, stream)

    def get_or_raise(
        self,
        url: str,
        params: Dict[str, Any] = None,
        non_error_status: Sequence[int] = None,
        stream: bool = False,
    ) -> "Response":
        return self.raise_on_error(self.get(url, params, stream=stream), non_error_status)

    def post(self, url: str, params: Dict[str, Any] = None, json: object = None, stream: bool = False) -> "Response":
        return self._request("POST", url, params, json, stream)

    def post_or_raise(
        self,
        url: str,
        params: Dict[str, Any] = None,
        json: object = None,
        non_error_status: Sequence[int] = None,
        stream: bool = False,
    ) -> "Response":
        return self.raise_on_error(self.post(url, params, json, stream=stream), non_error_status)

    def delete(self, url: str, params: Dict[str, Any] = None, stream: bool = False) -> "Response":
        return self._request("DELETE", url, params, None, stream)

    def delete_or_raise(
        self,
        url: str,
        params: Dict[str, Any] = None,
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

    def _request(
        self, method: str, url: str, params: Optional[Dict[str, Any]], json: object, stream: bool
    ) -> "Response":
        if not self._is_open:
            raise ValueError("Session is not open")

        self._auth_client.fetch_token_if_necessary()

        response = self.requests_session.request(
            method,
            self.api_url + url,
            params=params,
            json=json,
            stream=stream,
            headers={"Accept": "application/json"},
            auth=self._auth_client.requests_auth,
        )

        if response.status_code == 401:
            self._auth_client.fetch_token()
            response = self.requests_session.request(
                method,
                self.api_url + url,
                params=params,
                json=json,
                stream=stream,
                headers={"Accept": "application/json"},
                auth=self._auth_client.requests_auth,
            )
        return response

    def _create_metadata(self, data: Optional[Dict[str, Any]]) -> Metadata:
        return cast(Metadata, _Metadata(data, self._metadata_type_directory)) if data else {}

    def debug(self) -> None:
        # pylint: disable=W0613
        def print_response(response: Any, *args: Any, **kwargs: Any) -> None:
            print(response.request.url)
            print(response.status_code)
            print(response.json())

        # pylint: enable=W0613

        if len(self.requests_session.hooks["response"]) == 0:
            self.requests_session.hooks["response"].append(print_response)
