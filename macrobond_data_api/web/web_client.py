from typing import Optional, List, Tuple, Type
import json
import sys
import keyring

from macrobond_data_api.common import Client

from .session import Session as _Session
from .scope import Scope
from .web_api import WebApi
from .configuration import Configuration


class KeyringException(Exception):
    pass


def _get_credentials_from_keyring(service_name: str, username: Optional[str]) -> Tuple[str, str]:
    if username == "":
        raise ValueError('username is set to ""')

    keyring_name = keyring.get_keyring().name

    if sys.platform.startswith("darwin"):
        credentials = keyring.get_credential(service_name, Configuration._darwin_username)
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


# Not in use in this file
def _has_credentials_in_keyring(service_name: Optional[str] = None) -> bool:
    if not service_name:
        service_name = Configuration._default_service_name
    try:
        _get_credentials_from_keyring(service_name, None)
        return True
    except KeyringException:
        return False


def _try_get_proxy_from_keyring() -> Optional[str]:
    if isinstance(keyring.get_keyring(), keyring.backends.fail.Keyring):
        return None

    credentials = keyring.get_credential(Configuration._proxy_service_name, Configuration._proxy_username)
    if not credentials or credentials.password == "":
        return None
    return credentials.password


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

    configuration: Type[Configuration] = Configuration

    def __init__(
        self,
        username: str = None,
        password: str = None,
        scopes: List[Scope] = None,
        api_url: str = None,
        authorization_url: str = None,
        service_name: str = None,
        proxy: str = None,
    ) -> None:
        super().__init__()

        if service_name is None:
            service_name = Configuration._default_service_name

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
            username,
            password,
            *scopes,
            api_url=api_url,
            authorization_url=authorization_url,
            proxy=proxy,
        )

    @property
    def is_open(self) -> bool:
        return bool(self.__api)

    def open(self) -> "WebApi":
        if self.has_closed:
            raise ValueError("WebClient can not be reopend")
        if self.__api is None:
            self.__session._auth_client.fetch_token_if_necessary()
            self.__api = WebApi(self.__session)
        return self.__api

    def close(self) -> None:
        self.__session.close()
        self.__api = None
        self.has_closed = True
