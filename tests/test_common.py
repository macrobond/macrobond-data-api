# -*- coding: utf-8 -*-

# pylint: disable=invalid-name missing-function-docstring , missing-class-docstring , missing-module-docstring

import unittest
from typing import Type, Any, cast, List
from pathlib import Path
import json

from macrobond_financial.com import ComClient, ComApi
from macrobond_financial.web import WebClient, WebApi, Scope


class UserSecrets():

    api_url: str
    authorization_url: str
    client_id: str
    client_secret: str

    def __init__(self) -> None:
        guid = "314101f0-4c66-443c-9371-d2047861915d"
        home = str(Path.home())
        path = home + "\\AppData\\Roaming\\Microsoft\\UserSecrets\\" + guid + "\\secrets.json"
        file = open(path, encoding="utf-8")
        j = json.load(file)
        file.close()

        self.api_url = j['apiUrl']
        self.authorization_url = j['authorizationUrl']
        self.client_id = j['clientId']
        self.client_secret = j['clientSecret']


class UserSecretsSuite(unittest.TestCase):

    def test_user_secrets(self) -> None:
        us = UserSecrets()
        self.assertIsInstance(us.api_url, str, "'apiUrl' should be of type str")
        self.assertIsInstance(us.authorization_url, str, "'authorizationUrl' should be of type str")
        self.assertIsInstance(us.client_id, str, "'clientId' should be of type str")
        self.assertIsInstance(us.client_secret, str, "'clientSecret' should be of type str")


class TestCase(unittest.TestCase):

    com_client: ComClient = cast(ComClient, None)
    com_api: ComApi = cast(ComApi, None)

    web_client: WebClient = cast(WebClient, None)
    web_api: WebApi = cast(WebApi, None)

    _userSecrets: UserSecrets

    @classmethod
    def setUpClass(cls) -> None:
        cls._userSecrets = UserSecrets()

    def setUp(self) -> None:
        self.set_up_com_client()
        self.set_up_web_client()

    def tearDown(self) -> None:
        self.com_client.close()
        self.web_client.close()

    def set_up_com_client(self) -> None:
        self.com_client = ComClient()
        self.com_api = self.com_client.open()

    def set_up_web_client(self, *scopes: Scope) -> None:
        if self.web_client is not None:
            self.web_client.close()
        self.web_client = WebClient(
            self._userSecrets.client_id,
            self._userSecrets.client_secret,
            *scopes,
            api_url=self._userSecrets.api_url,
            authorization_url=self._userSecrets.authorization_url
        )
        self.web_api = self.web_client.open()

    def assertType(self, val: Any, test_type: Type) -> None:
        self.assertEqual(type(val), test_type)

    def assertDescendant(self, val: Any, test_type: Type) -> None:
        self.assertTrue(
            isinstance(val, test_type),
            val.__class__.__name__ + " is not a descendant of " + test_type.__name__
        )

    def assertValueComparison(self, obj1: object, obj2: object) -> None:
        dir1 = list(filter(lambda s: not s.startswith('_'), dir(obj1)))
        dir2 = list(filter(lambda s: not s.startswith('_'), dir(obj2)))
        intersection = [value for value in dir1 if value in dir2]
        for name in intersection:
            if hasattr(obj1, name) and hasattr(obj2, name):
                val1 = getattr(obj1, name)
                val2 = getattr(obj2, name)
                self.assertEqual(val1, val2, name)
            elif hasattr(obj1, name) or hasattr(obj2, name):
                self.fail()

    def assertAttributs(
        self, obj1: object, obj2: object, ignore: List[str] = None
    ) -> None:
        if ignore is None:
            ignore = []
        ignore_not_none: List[str] = ignore

        def name_filter(s: str) -> bool:
            return not s.startswith('_') and s not in ignore_not_none

        list1 = sorted(filter(name_filter, dir(obj1)))
        list2 = sorted(filter(name_filter, dir(obj2)))

        self.assertListEqual(list1, list2)

        for name in list1:

            val1 = getattr(obj1, name)
            val2 = getattr(obj2, name)

            self.assertEqual(val1, val2, name)
