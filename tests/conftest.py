from datetime import datetime, timezone
import os
from typing import Any, Sequence, Union
import collections.abc
import warnings
from pyparsing import Generator

from pytest import fixture, FixtureRequest
import pandas  # type: ignore

from macrobond_data_api.web.session import Session
from macrobond_data_api.common import Api
from macrobond_data_api.web import WebClient, WebApi
from macrobond_data_api.web.web_client import API_URL_DEFAULT, AUTHORIZATION_URL_DEFAULT
from macrobond_data_api.com import ComClient, ComApi


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

        with open(conf_path, "r", encoding="utf-8") as f:
            conf: dict = {}
            exec(f.read(), conf)  # pylint: disable=exec-used
            api_url = conf.get("api_url", API_URL_DEFAULT)
            authorization_url = conf.get("authorization_url", AUTHORIZATION_URL_DEFAULT)
            yield WebClient(api_url=api_url, authorization_url=authorization_url)
            return

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
    return _test


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


def _test(
    web: Union[Sequence[object], object],
    com: Union[Sequence[object], object],
    can_be_none: bool = False,
    can_be_empty: bool = False,
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
            if isinstance(web_obj.metadata[key], datetime):
                web_datetime = _remove_microsecond(web_obj.metadata[key])
                if web_datetime.tzinfo:
                    web_datetime = web_datetime.astimezone(timezone.utc)

                com_datetime = _remove_microsecond(com_obj.metadata[key])
                if com_datetime.tzinfo:
                    com_datetime = com_datetime.astimezone(timezone.utc)

                if web_datetime != com_datetime:
                    diff = (web_datetime - com_datetime).total_seconds()
                    if diff == 0:
                        continue

                assert web_datetime == com_datetime, "key " + key
            else:
                assert web_obj.metadata[key] == com_obj.metadata[key], "key " + key

        web_obj.metadata = {}
        com_obj.metadata = {}
