from typing import Any
import warnings
from pyparsing import Generator

from pytest import fixture, FixtureRequest
import pandas  # type: ignore

from macrobond_data_api.common import Api
from macrobond_data_api.web import WebClient, WebApi
from macrobond_data_api.com import ComClient, ComApi


@fixture(autouse=True, scope="session")
def _conf_pandas() -> None:
    pandas.set_option("display.max_rows", 500)
    pandas.set_option("display.max_columns", 500)
    pandas.set_option("display.width", 1000)


@fixture(scope="session", name="web_client")
def _web_client_fixture() -> Generator[WebClient, None, None]:
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
