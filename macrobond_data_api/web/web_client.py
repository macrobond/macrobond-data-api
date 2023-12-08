from typing import Optional, List, Tuple
import json
import sys
import keyring

from macrobond_data_api.common import Client

from .session import Session as _Session, API_URL_DEFAULT, AUTHORIZATION_URL_DEFAULT
from .scope import Scope
from .web_api import WebApi

DEFAULT_SERVICE_NAME = AUTHORIZATION_URL_DEFAULT
DARWIN_USERNAME = "Macrobond"

DEFAULT_PROXY_SERVICE_NAME = "MacrobondApiHttpProxy"
PROXY_USERNAME = "MacrobondApiHttpProxy"


class KeyringException(Exception):
    pass


def _get_credentials_from_keyring(  # pylint: disable=too-many-branches
    service_name: str, username: Optional[str]
) -> Tuple[str, str]:
    if username == "":
        raise ValueError('username is set to ""')

    keyring_name = keyring.get_keyring().name

    if sys.platform.startswith("darwin"):
        credentials = keyring.get_credential(service_name, DARWIN_USERNAME)
        if not credentials:
            raise KeyringException(f"Can not find the key in keyring {keyring_name}")

        json_obj = json.loads(credentials.password)

        if not isinstance(json_obj, dict):
            raise KeyringException(f"Bad format, password is not a json objekt in keyring {keyring_name}")

        if "username" not in json_obj:
            raise KeyringException(f"Bad format, the json objekt is missing username in keyring {keyring_name}")

        if "password" not in json_obj:
            raise KeyringException(f"Bad format, the json objekt is missing password in keyring  {keyring_name}")

        if username is None:
            username = json_obj["username"]

        password = json_obj["password"]
    else:
        credentials = keyring.get_credential(service_name, None)

        if credentials is None:
            raise KeyringException(f"Can not find the key in keyring {keyring.get_keyring()}")

        if username is None:
            username = credentials.username

        password = credentials.password

    if username == "":
        raise KeyringException(f'Username is set to "" in keyring {keyring_name}')

    if password == "":
        raise KeyringException(f'Password is set to "" in keyring {keyring_name}')

    return username, password


def _has_credentials_in_keyring(service_name: Optional[str] = None) -> bool:
    if not service_name:
        service_name = DEFAULT_SERVICE_NAME
    try:
        _get_credentials_from_keyring(service_name, None)
        return True
    except KeyringException:
        return False


def _try_get_proxy_from_keyring() -> Optional[str]:
    credentials = keyring.get_credential(DEFAULT_PROXY_SERVICE_NAME, PROXY_USERNAME)
    if not credentials or credentials.password == "":
        return None
    return credentials.password


def _has_proxy_in_keyring() -> bool:
    return _try_get_proxy_from_keyring() is not None


class WebClient(Client["WebApi"]):
    """
    WebClient to get data from the web

    Parameters
    ----------
    username : str, optional
        The username to use for authentication.
        If not specified, an attempt is made to get the credentials from the keyring

    password : str, optional
        The password to use for authentication.
        If not specified, an attempt is made to get the credentials from the keyring

    scopes : List[str], optional
        A list of scopes to request as part of the authorization.
        If not specified, all available scopes will be requested.
        The common scopes requires are "macrobond_web_api.read_mb" and "macrobond_web_api.search_mb"

    api_url : str, optional
        The URL of the API.
        If not specified, the default URL will be used, which is what you want in most cases.

    authorization_url : str, optional
        The URL of the authorization server.
        If not specified, the default URL will be used, which is what you want in most cases.

    proxy : str, optional
        For a HTTPS Proxy use `https://10.10.1.10:1080` or `https://user:pass@10.10.1.10:1080`
        For a HTTP Proxy use `http://10.10.1.10:1080` or `http://user:pass@10.10.1.10:1080`
        For a Socks5 Proxy use `socks5://user:pass@host:port`

    Returns
    -------
    WebClient
        The WebClient instance

    Examples
    -------
    ```python
    # use credentials stored in the keyring
    with WebClient() as api:
        # use the api here
    ```
    ```python
    with WebClient('client id', 'client secret') as api:
        # use the api here
    ```
    """

    def __init__(
        self,
        username: str = None,
        password: str = None,
        scopes: List[Scope] = None,
        api_url: str = API_URL_DEFAULT,
        authorization_url: str = AUTHORIZATION_URL_DEFAULT,
        service_name: str = DEFAULT_SERVICE_NAME,
        proxy: str = None,
    ) -> None:
        super().__init__()

        if password is None:
            credentials = _get_credentials_from_keyring(service_name, username)
            username = credentials[0]
            password = credentials[1]
        else:
            if username is None:
                raise ValueError("username is None")

        if scopes is None:
            scopes = []

        if proxy is None:
            proxy = _try_get_proxy_from_keyring()

        self.has_closed = False
        self.__api: Optional["WebApi"] = None
        self.__session = _Session(
            username, password, *scopes, api_url=api_url, authorization_url=authorization_url, proxy=proxy
        )

    @property
    def is_open(self) -> bool:
        return bool(self.__api)

    def open(self) -> "WebApi":
        if self.has_closed:
            raise ValueError("WebClient can not be reopend")
        if self.__api is None:
            self.__session.fetch_token()
            self.__api = WebApi(self.__session)
        return self.__api

    def close(self) -> None:
        self.__session.close()
        self.__api = None
        self.has_closed = True
