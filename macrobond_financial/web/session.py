# -*- coding: utf-8 -*-

from typing import Callable, Optional, Any, TYPE_CHECKING

from authlib.integrations.requests_client import OAuth2Session  # type: ignore

from .web_typs import (
    MetadataMethods,
    SearchMethods,
    SeriesMethods,
    SeriesTreeMethods,
    SessionHttpException,
)

from .scope import Scope

API_URL_DEFAULT = "https://api.macrobondfinancial.com/"
AUTHORIZATION_URL_DEFAULT = "https://apiauth.macrobondfinancial.com/mbauth/"

if TYPE_CHECKING:  # pragma: no cover
    from requests import Response  # type: ignore

__pdoc__ = {
    "Session.__init__": False,
}


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
        client_id: str,
        client_secret: str,
        *scopes: Scope,
        api_url: str = API_URL_DEFAULT,
        authorization_url: str = API_URL_DEFAULT,
        test_auth2_session: Any = None
    ) -> None:
        self.__token_endpoint: Optional[str] = None

        if not authorization_url.endswith("/"):
            authorization_url = authorization_url + "/"
        self.__authorization_url = authorization_url

        if not api_url.endswith("/"):
            api_url = api_url + "/"
        self.__api_url = api_url

        scopes_str_list = list(map(lambda s: s.value, scopes))
        if test_auth2_session is None:
            self.__auth2_session = OAuth2Session(
                client_id, client_secret, scope=scopes_str_list
            )
        else:
            self.__auth2_session = test_auth2_session

        self.__metadata = MetadataMethods(self)
        self.__search = SearchMethods(self)
        self.__series = SeriesMethods(self)
        self.__series_tree = SeriesTreeMethods(self)

    def close(self) -> None:
        self.auth2_session.close()

    def fetch_token(self) -> None:
        if self.token_endpoint is None:
            self.__token_endpoint = self.discovery(self.authorization_url)
        self.auth2_session.fetch_token(self.token_endpoint)

    def get(self, url: str, params: dict = None) -> "Response":
        def http():
            return self.auth2_session.get(url=self.api_url + url, params=params)

        return self.__if_status_code_401_fetch_token_and_retry(http)

    def get_or_raise(self, url: str, params: dict = None) -> "Response":
        response = self.get(url, params)
        if response.status_code != 200:
            raise SessionHttpException(response)
        return response

    def post(self, url: str, params: dict = None, json: object = None) -> "Response":
        def http():
            return self.auth2_session.post(
                url=self.api_url + url, params=params, json=json
            )

        return self.__if_status_code_401_fetch_token_and_retry(http)

    def post_or_raise(
        self, url: str, params: dict = None, json: object = None
    ) -> "Response":
        response = self.post(url, params, json)
        if response.status_code != 200:
            raise SessionHttpException(response)
        return response

    def discovery(self, url: str) -> str:
        response = self.auth2_session.request(
            "get", url + ".well-known/openid-configuration", True
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
        response = http()
        if response.status_code == 401:
            self.fetch_token()
            response = http()
        return response
