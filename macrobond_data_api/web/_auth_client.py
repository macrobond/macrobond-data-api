import time
from typing import Any, Dict, Sequence, Optional, TYPE_CHECKING

from .auth_error import AuthFetchTokenError, AuthDiscoveryError, AuthInvalidCredentialsError

if TYPE_CHECKING:  # pragma: no cover
    from .scope import Scope
    from .session import Session
    from requests.models import PreparedRequest


class _RequestsAuth:
    def __init__(self) -> None:
        self.access_token = ""

    def __call__(self, r: "PreparedRequest") -> "PreparedRequest":
        r.headers["Authorization"] = "Bearer " + self.access_token
        return r


class _AuthClient:

    def __init__(
        self, username: str, password: str, scope: Sequence["Scope"], authorization_url: str, session: "Session"
    ) -> None:
        self._username = username
        self._password = password
        self.scope = " ".join((str(x) for x in scope))
        self.authorization_url = authorization_url
        self.token_endpoint: Optional[str] = None
        self.session = session
        self.requests_auth = _RequestsAuth()
        self.token_response: Optional[Dict[str, Any]] = None
        self.leeway = 60
        self.expires_at: Optional[int] = None
        self.fetch_token_get_time = time.time
        self.is_expired_get_time = time.time

    def fetch_token_if_necessary(self) -> bool:
        if self._is_expired():
            self.fetch_token()
            return True
        return False

    def fetch_token(self) -> None:
        if self.token_endpoint is None:
            self.token_endpoint = self._discovery(self.authorization_url)

        self._fetch_token(self.token_endpoint)

    def _fetch_token(self, token_endpoint: str) -> None:
        payload = {
            "grant_type": "client_credentials",
            "client_id": self._username,
            "client_secret": self._password,
            "scope": self.scope,
        }
        response = self.session.requests_session.post(
            token_endpoint, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code not in [200, 400]:
            raise AuthFetchTokenError("status code is not 200 or 400")

        try:
            json = self.token_response = response.json()
        except BaseException as base_exception:
            raise AuthFetchTokenError("not valid json") from base_exception

        if not isinstance(json, dict):
            raise AuthFetchTokenError("no root obj in json")

        if response.status_code == 400:
            error = json.get("error")
            if error == "invalid_client":
                raise AuthInvalidCredentialsError("invalid client credentials")
            if isinstance(error, str):
                raise AuthFetchTokenError("error: " + error)
            raise AuthFetchTokenError("no error in response")

        if json.get("token_type") and json["token_type"] != "Bearer":
            raise AuthFetchTokenError("token_type is not Bearer")

        if json.get("expires_at"):
            self.expires_at = int(json["expires_at"])
        elif json.get("expires_in"):
            self.expires_at = int(self.fetch_token_get_time()) + int(json["expires_in"])
        else:
            raise AuthFetchTokenError("no expires_at or expires_in")

        if not json.get("access_token"):
            raise AuthFetchTokenError("No access_token")

        self.requests_auth.access_token = json["access_token"]

    def _discovery(self, url: str) -> str:

        response = self.session.requests_session.get(url + ".well-known/openid-configuration")
        if response.status_code != 200:
            raise AuthDiscoveryError("status code is not 200")

        try:
            json: Optional[Dict[str, Any]] = response.json()
        except BaseException as base_exception:
            raise AuthDiscoveryError("not valid json.") from base_exception

        if not isinstance(json, dict):
            raise AuthDiscoveryError("no root obj in json.")

        token_endpoint: Optional[str] = json.get("token_endpoint")
        if token_endpoint is None:
            raise AuthDiscoveryError("token_endpoint in root obj.")

        return token_endpoint

    def _is_expired(self) -> bool:
        if not self.expires_at:
            return True
        expiration_threshold = self.expires_at - self.leeway
        return expiration_threshold < self.is_expired_get_time()
