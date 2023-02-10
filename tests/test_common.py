# pylint: disable=invalid-name missing-function-docstring , missing-class-docstring , missing-module-docstring

from unittest import TestCase as UnittestTestCase  # type: ignore
from typing import Optional, Callable, Any
import warnings
import io
import sys


import pandas  # type: ignore

from macrobond_data_api.com import ComClient, ComApi
from macrobond_data_api.web import WebClient, WebApi


pandas.set_option("display.max_rows", 500)
pandas.set_option("display.max_columns", 500)
pandas.set_option("display.width", 1000)


class TestCase(UnittestTestCase):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(TestCase, self).__init__(*args, **kwargs)
        self.__com_client: Optional[ComClient] = None
        self.__com_api: Optional[ComApi] = None
        self.__web_client: Optional[WebClient] = None
        self.__web_api: Optional[WebApi] = None

    def assertNoWarnings(self, mef: Callable) -> None:
        captured_output_stdout = io.StringIO()
        sys.stdout = captured_output_stdout

        captured_output_stderr = io.StringIO()
        sys.stderr = captured_output_stderr

        with warnings.catch_warnings(record=True) as wlist:
            warnings.simplefilter("always")
            mef()
            self.assertEqual(len(wlist), 0, "\n\n".join(map(str, wlist)))

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        stdout = captured_output_stdout.getvalue()
        self.assertEqual(stdout, "", "captured_output_stdout")

        stderr = captured_output_stderr.getvalue()
        self.assertEqual(stderr, "", "captured_output_stderr")

    @property
    def web_client(self) -> WebClient:
        if self.__web_client is None:
            self.__web_client = WebClient()

        return self.__web_client

    @property
    def web_api(self) -> WebApi:
        if self.__web_api is None:
            self.__web_api = self.web_client.open()
        return self.__web_api

    @property
    def com_client(self) -> ComClient:
        if self.__com_client is None:
            self.__com_client = ComClient()
        return self.__com_client

    @property
    def com_api(self) -> ComApi:
        if self.__com_api is None:
            self.__com_api = self.com_client.open()
        return self.__com_api

    def tearDown(self) -> None:
        if self.__web_client:
            self.__web_client.close()
        self.__web_client = None

        if self.__com_client:
            self.__com_client.close()
        self.__com_client = None
