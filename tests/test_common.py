# -*- coding: utf-8 -*-

# pylint: disable=invalid-name missing-function-docstring , missing-class-docstring , missing-module-docstring

import os
import os.path
from unittest import TestCase as UnittestTestCase  # type: ignore
from pathlib import Path
from typing import Optional
import json

import pandas  # type: ignore

from macrobond_financial.com import ComClient, ComApi
from macrobond_financial.web import WebClient, WebApi

from macrobond_financial.common import Credentials


pandas.set_option("display.max_rows", 500)
pandas.set_option("display.max_columns", 500)
pandas.set_option("display.width", 1000)


def get_credentials() -> Credentials:
    guid = "314101f0-4c66-443c-9371-d2047861915d"

    dir_path = os.path.join(
        Path.home(), "AppData", "Roaming", "Microsoft", "UserSecrets", guid
    )

    path = os.path.join(dir_path, "secrets.json")

    if not os.path.exists(path):
        os.makedirs(dir_path, exist_ok=True)
        with open(path, "w+", encoding="utf-8") as f:
            json_str = json.dumps(
                {
                    "apiUrl": "https://api.macrobondfinancial.com/",
                    "authorizationUrl": "https://apiauth.macrobondfinancial.com/mbauth",
                    "clientId": "",
                    "clientSecret": "",
                },
                indent=4,
            )
            f.write(json_str)
        raise Exception(
            "Credentials has been created at "
            + path
            + ", add your clientId amd clientSecret"
        )

    return Credentials([path])


class TestCase(UnittestTestCase):

    __credentials: Optional[Credentials] = None

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self.__com_client: Optional[ComClient] = None
        self.__com_api: Optional[ComApi] = None
        self.__web_client: Optional[WebClient] = None
        self.__web_api: Optional[WebApi] = None

    @property
    def web_client(self) -> WebClient:
        if TestCase.__credentials is None:
            TestCase.__credentials = get_credentials()

        if self.__web_client is None:
            credentials = TestCase.__credentials
            self.__web_client = WebClient(credentials)

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
