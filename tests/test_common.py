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


pandas.set_option("display.max_rows", 500)
pandas.set_option("display.max_columns", 500)
pandas.set_option("display.width", 1000)


class UserSecrets:
    def __init__(self) -> None:
        with open(self.path(), encoding="utf-8") as f:
            j = json.load(f)

        self.api_url: str = j["apiUrl"]
        self.authorization_url: str = j["authorizationUrl"]
        self.client_id: str = j["clientId"]
        self.client_secret: str = j["clientSecret"]

        if self.client_id == "":
            raise Exception(
                'UserSecrets.client_id is "", add client_id to ' + self.path()
            )
        if self.client_secret == "":
            raise Exception(
                'UserSecrets.client_secret is "", add client_secret to ' + self.path()
            )

    @classmethod
    def guid(cls) -> str:
        return "314101f0-4c66-443c-9371-d2047861915d"

    @classmethod
    def dir_path(cls) -> str:
        return os.path.join(
            Path.home(), "AppData", "Roaming", "Microsoft", "UserSecrets", cls.guid()
        )

    @classmethod
    def path(cls) -> str:
        return os.path.join(cls.dir_path(), "secrets.json")

    @classmethod
    def exists(cls) -> bool:
        return os.path.exists(cls.path())

    @classmethod
    def write_example(cls) -> None:
        os.makedirs(cls.dir_path(), exist_ok=True)
        with open(cls.path(), "w+", encoding="utf-8") as f:
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


class TestCase(UnittestTestCase):

    __userSecrets: Optional[UserSecrets] = None

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self.__com_client: Optional[ComClient] = None
        self.__com_api: Optional[ComApi] = None
        self.__web_client: Optional[WebClient] = None
        self.__web_api: Optional[WebApi] = None

    @property
    def web_client(self) -> WebClient:
        if TestCase.__userSecrets is None:
            if not UserSecrets.exists():
                UserSecrets.write_example()
                raise Exception(
                    "UserSecrets has been created at "
                    + UserSecrets.path()
                    + ", add your clientId amd clientSecret"
                )
            TestCase.__userSecrets = UserSecrets()

        if self.__web_client is None:
            user_secrets = TestCase.__userSecrets
            self.__web_client = WebClient(
                user_secrets.client_id,
                user_secrets.client_secret,
                api_url=user_secrets.api_url,
                authorization_url=user_secrets.authorization_url,
            )

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
