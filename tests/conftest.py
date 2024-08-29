# pylint: disable = unused-argument

from datetime import datetime, timezone
from unittest.mock import Mock
import os
from typing import Any, Sequence, Union, Generator, Dict, List, Tuple
import collections.abc
import warnings

from json import dumps as json_dump

from authlib.integrations.requests_client import OAuth2Session

from filelock import FileLock

from pytest import fixture, FixtureRequest, Session as PytestSession
import pandas

from requests import Response
from requests.adapters import BaseAdapter
from requests.models import Response as ResponseModel

from macrobond_data_api.web.session import Session
from macrobond_data_api.common import Api
from macrobond_data_api.web import WebClient, WebApi
from macrobond_data_api.com import ComClient, ComApi


def pytest_sessionstart(session: PytestSession) -> None:
    print("Running in timezone:", datetime.now().astimezone().strftime("%Z %z"))


class MockAdapterBuilder:

    urls: List[str] = []
    responses: List[Response] = []

    # this are just test tokens !
    test_token_1 = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoidGVzdDEifQ.fkwEean9sw5NhO2pRmRpQgEiTWYeQwgVNl5QxQLeYPo"
    )
    test_token_2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    test_token_3 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoidGVzdDMiLCJleHAiOjE3MjQ4NDIxMjh9.e5qnFRDhBhpELGsjbFY7W85ESML4HVmiRf0un3XfIHo"

    def build(self) -> Tuple["MockAdapter", WebApi]:
        mockAdapter = MockAdapter(self.responses, self.urls)

        auth_session = OAuth2Session("username", "password", scope=[])
        auth_session.mount("https://", mockAdapter)

        session = Session("", "", test_auth2_session=auth_session)

        webApi = WebApi(session)

        return mockAdapter, webApi

    def add_response(self, url: str, status_code: int, json: Any = None) -> "MockAdapterBuilder":
        response = ResponseModel()
        response.status_code = status_code
        response.history = []
        if json:
            response._content = json_dump(json).encode()

        self.responses.append(response)
        self.urls.append(url)

        return self

    def add_discovery(self) -> "MockAdapterBuilder":
        return self.add_response(
            "https://apiauth.macrobondfinancial.com/mbauth/.well-known/openid-configuration",
            200,
            {
                "token_endpoint": "https://get_a_nice_token",
            },
        )

    def add_series_response(self, name: str, url: str = None) -> "MockAdapterBuilder":
        if url is None:
            url = f"https://api.macrobondfinancial.com/v1/series/fetchseries?n={name}"
        return self.add_response(
            url,
            200,
            [
                {
                    "dates": ["2021-01-01", "2021-01-02"],
                    "values": [1.0, 2.0],
                    "metadata": {"PrimName": name},
                }
            ],
        )

    def add_token(self, access_token: str, expires_in: int = None) -> "MockAdapterBuilder":
        if expires_in is None:
            expires_in = 3600
        return self.add_response(
            "https://get_a_nice_token/",
            200,
            {
                "access_token": access_token,
                "expires_in": expires_in,
                "token_type": "Bearer",
                "scope": "mb.test",
            },
        )


class MockAdapter(BaseAdapter):

    def __init__(self, responses: List[Response], urls: List[str]) -> None:
        self.mock = Mock()
        self.mock.send.side_effect = responses
        self.index = 0
        self.urls = urls

        assert len(responses) == len(urls)

        super().__init__()

    def send(
        self,
        request: Any,
        stream: Any = False,
        timeout: Any = None,
        verify: Any = True,
        cert: Any = None,
        proxies: Any = None,
    ) -> Response:

        if self.index >= len(self.urls):
            raise ValueError("To many requests url:", request.url)

        assert self.urls[self.index] == request.url

        self.index += 1

        response = self.mock.send()
        assert response is not None
        return response

    def close(self) -> None:
        pass


@fixture(scope="function", name="get_mock_adapter_builder")
def _get_mock_adapter_builder() -> Generator[MockAdapterBuilder, None, None]:
    yield MockAdapterBuilder()


class _ConfTest:

    def __init__(self, conf_path: str) -> None:
        conf: Dict[str, Any] = {}
        with open(conf_path, "r", encoding="utf-8") as f:
            exec(f.read(), conf)  # pylint: disable=exec-used

        self.api_url = conf.get("api_url", Session.configuration._default_api_url)
        self.authorization_url = conf.get("authorization_url", Session.configuration._default_authorization_url)
        self.username = conf.get("username", None)
        self.password = conf.get("password", None)


@fixture(autouse=True, scope="session")
def _conf_pandas() -> None:
    pandas.set_option("display.max_rows", 500)
    pandas.set_option("display.max_columns", 500)
    pandas.set_option("display.width", 1000)


@fixture(scope="session", name="web_client")
def _web_client_fixture() -> Generator[WebClient, None, None]:
    conf_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), "_conftest.py")

    if os.path.exists(conf_path):

        def test_is_https_url(self: "Session", url: str) -> bool:  # pylint: disable=unused-argument
            return True

        Session._is_https_url = test_is_https_url  # type: ignore

        conf = _ConfTest(conf_path)

        yield WebClient(
            api_url=conf.api_url,
            authorization_url=conf.authorization_url,
            username=conf.username,
            password=conf.password,
        )
    else:
        yield WebClient()


@fixture(scope="session", name="web")
def _web_fixture(web_client: WebClient) -> Generator[WebApi, None, None]:  # pylint: disable=redefined-outer-name
    with web_client as api:
        yield api


@fixture(scope="session", name="com_client")
def _com_client_fixture() -> Generator[ComClient, None, None]:
    yield ComClient()


@fixture(scope="session", name="com")
def _com_fixture(com_client: ComClient) -> Generator[ComApi, None, None]:  # pylint: disable=redefined-outer-name
    with com_client as api:
        yield api


@fixture(scope="session", name="api")
def _api(request: FixtureRequest) -> Api:
    return request.getfixturevalue(request.param)


@fixture(scope="function", name="lock_test")
def _test_lock() -> Generator[None, None, None]:
    path = os.path.join(os.getcwd(), "tests", "py_test.lock")
    with FileLock(path, timeout=30):
        yield None


@fixture(scope="function", name="assert_no_warnings")
def _assert_no_warnings(capsys: Any) -> Generator[None, None, None]:
    with warnings.catch_warnings(record=True) as wlist:
        warnings.simplefilter("always")
        try:
            yield None
        finally:
            assert len(wlist) == 0, "\n\n".join(str(x) for x in wlist)

            captured = capsys.readouterr()
            assert captured.out == ""
            assert captured.err == ""


@fixture(autouse=True, scope="function")
def _assert_no_warnings_all(capsys: Any) -> Generator[None, None, None]:
    with warnings.catch_warnings(record=True) as wlist:
        warnings.simplefilter("always")
        try:
            yield None
        finally:
            assert len(wlist) == 0, "\n\n".join(str(x) for x in wlist)

            captured = capsys.readouterr()
            assert captured.out == ""
            assert captured.err == ""


@fixture(scope="session", name="test_metadata")
def _test_metadata() -> Any:
    return _test_metadata_implment


def _remove_microsecond(datetime_: datetime) -> datetime:
    return datetime(
        datetime_.year,
        datetime_.month,
        datetime_.day,
        datetime_.hour,
        datetime_.minute,
        datetime_.second,
        # web_vintage.metadata[key].microsecond,
        tzinfo=datetime_.tzinfo,
    )


def _test_metadata_implment(
    web: Union[Sequence[object], object],
    com: Union[Sequence[object], object],
    can_be_none: bool = False,
    can_be_empty: bool = False,
    ignore_keys: Sequence[object] = None,
) -> None:
    if ignore_keys is None:
        ignore_keys = []

    if not isinstance(web, collections.abc.Sequence):
        web = [web]
        assert not isinstance(com, collections.abc.Sequence)

    if not isinstance(com, collections.abc.Sequence):
        com = [com]
        assert isinstance(web, collections.abc.Sequence)

    for web_obj, com_obj in zip(web, com):
        if can_be_none and web_obj.metadata is None and com_obj.metadata is None:
            continue

        keys = list(set(web_obj.metadata.keys()) & set(com_obj.metadata.keys()))
        keys.sort()

        if len(keys) == 0:
            if can_be_empty:
                continue

            assert len(keys) != 0

        if "DisplayUnit" in keys:
            keys.remove("DisplayUnit")

        for key in keys:
            if key in ignore_keys:
                continue

            if isinstance(web_obj.metadata[key], datetime):
                web_datetime = _remove_microsecond(web_obj.metadata[key])
                if web_datetime.tzinfo:
                    web_datetime = web_datetime.astimezone(timezone.utc)

                com_datetime = _remove_microsecond(com_obj.metadata[key])
                if com_datetime.tzinfo:
                    com_datetime = com_datetime.astimezone(timezone.utc)

                if web_datetime != com_datetime:
                    try:
                        diff = (web_datetime - com_datetime).total_seconds()
                        if diff == 0:
                            continue
                    except TypeError:
                        ...
                assert web_datetime == com_datetime, "key " + key
            else:
                assert web_obj.metadata[key] == com_obj.metadata[key], "key " + key

        web_obj.metadata = {}
        com_obj.metadata = {}
