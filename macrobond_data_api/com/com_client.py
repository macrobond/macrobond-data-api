# -*- coding: utf-8 -*-

import sys

from typing import TYPE_CHECKING, List, Optional

from macrobond_data_api.common import Client

from .com_api import ComApi

if TYPE_CHECKING:  # pragma: no cover
    from .com_types import Connection

_win32com_import_error: Optional[ImportError] = None
try:
    from win32com import client as _client  # type: ignore
except ImportError as ex:
    _win32com_import_error = ex

_pywintypes_import_error: Optional[ImportError] = None
try:
    from pywintypes import com_error  # type: ignore
except ImportError as ex:
    _pywintypes_import_error = ex

try:
    from winreg import OpenKey, QueryValueEx, HKEY_CLASSES_ROOT, HKEY_CURRENT_USER  # type: ignore
except ImportError:
    ...


class ComClient(Client["ComApi"]):
    """
    ComClient to get data via the Macrobond desktop API

    Returns
    -------
    ComClient
        The ComClient instance

    Examples
    -------
    ```python
    with ComClient() as api:
        # use the api here
    ```
    """

    def __init__(self) -> None:
        super().__init__()
        self.__api: Optional["ComApi"] = None

    @property
    def is_open(self) -> bool:
        return bool(self.__api)

    def open(self) -> "ComApi":
        if _win32com_import_error:
            raise _win32com_import_error

        if _pywintypes_import_error:
            raise _pywintypes_import_error

        if self.__api is None:
            try:
                connection: "Connection" = _client.Dispatch("Macrobond.Connection")
            except com_error:

                hints: List[str] = []

                sub_key = "CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32"
                try:
                    with OpenKey(
                        HKEY_CLASSES_ROOT,
                        sub_key,
                    ) as regkey:
                        QueryValueEx(regkey, "Assembly")
                except OSError:
                    hints.append(
                        (
                            'Could not find the registration key "HKEY_CLASSES_ROOT\\'
                            + sub_key
                            + '\\Assembly",\nThis indicates that Macrobond is not installed.'
                        )
                    )

                sub_key = "Software\\Macrobond Financial\\Communication\\Connector"
                try:
                    with OpenKey(HKEY_CURRENT_USER, sub_key) as regkey:
                        QueryValueEx(regkey, "UserName")
                except OSError:
                    hints.append(
                        (
                            'Could not find the registration key "HKEY_CURRENT_USER\\'
                            + sub_key
                            + '\\UserName",\nThis indicates that Macrobond is not logged in.'
                        )
                    )

                if len(hints) != 0:
                    print("\n\nERROR in ComClient.open()", file=sys.stderr)

                for hint in hints:
                    print("\n" + hint, file=sys.stderr)

                if len(hints) != 0:
                    print("", file=sys.stderr)

                raise

            self.__api = ComApi(connection)
        return self.__api

    def close(self) -> None:
        """
        free all resources used by the Macrobond API.
        Opening and closing sessions can be slow,
        so it is usually not a good idea to open and close them for each request
        """
        if self.__api:
            self.__api.connection.Close()
            self.__api = None
