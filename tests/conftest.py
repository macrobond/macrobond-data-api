# pylint: disable = unused-argument

from datetime import datetime, timezone
import os
from typing import Any, Sequence, Union, Generator, Dict
import collections.abc
import warnings

from filelock import FileLock

from pytest import fixture, FixtureRequest, Session as PytestSession

from numpy.testing import assert_approx_equal

import pandas

from macrobond_data_api.web.session import Session
from macrobond_data_api.common import Api
from macrobond_data_api.web import WebClient, WebApi
from macrobond_data_api.com import ComClient, ComApi

from .mock_adapter_builder import MockAdapterBuilder


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "no_account: marks tests that can run without a user, and without internet connection",
    )


def pytest_sessionstart(session: PytestSession) -> None:
    print("Running in timezone:", datetime.now().astimezone().strftime("%Z %z"))


class _ConfTest:

    def __init__(self, conf_path: str) -> None:
        conf: Dict[str, Any] = {}
        with open(conf_path, "r", encoding="utf-8") as f:
            exec(f.read(), conf)  # pylint: disable=exec-used

        self.api_url = conf.get("API_URL", Session.configuration._default_api_url)
        self.authorization_url = conf.get("AUTHORIZATION_URL", Session.configuration._default_authorization_url)
        self.username = conf.get("USERNAME", None)
        self.password = conf.get("PASSWORD", None)


@fixture(scope="function", name="mab")
def _test_mab() -> Generator[MockAdapterBuilder, None, None]:
    mab = MockAdapterBuilder()
    yield mab
    mab.assert_this()


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


@fixture(scope="session", name="test_values")
def _test_values() -> Any:
    return _test_values_implment


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


def _test_values_implment(
    web_values: Sequence[Union[float, None]],
    com_values: Sequence[Union[float, None]],
) -> None:
    assert isinstance(web_values, collections.abc.Sequence)
    assert isinstance(com_values, collections.abc.Sequence)

    assert len(web_values) == len(com_values)

    for i, _ in enumerate(web_values):
        if web_values[i] is None and com_values[i] is None:
            continue
        assert_approx_equal(web_values[i], com_values[i], significant=16)
        web_values[i] = com_values[i]


def _test_metadata_implment(
    web: Union[Sequence[object], object],
    com: Union[Sequence[object], object],
    can_be_none: bool = False,
    can_be_empty: bool = False,
    ignore_keys: Sequence[object] = None,
) -> None:
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
            if ignore_keys and key in ignore_keys:
                continue

            if isinstance(web_obj.metadata[key], datetime):
                _test_meta_datetime(web_obj, com_obj, key)
            else:
                assert (
                    web_obj.metadata[key] == com_obj.metadata[key]
                ), f"key {key} - web {str(web_obj.metadata[key])} != com {str(com_obj.metadata[key])}"

        web_obj.metadata = {}
        com_obj.metadata = {}


def _test_meta_datetime(web_obj: Any, com_obj: Any, key: str) -> None:
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
                return
        except TypeError:
            ...
    assert web_datetime == com_datetime, f"key {key} - web {str(web_datetime)} != com {str(com_datetime)}"
