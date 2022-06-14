# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING, Optional

from macrobond_financial.common import Client

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
    from pywintypes import com_error
except ImportError as ex:
    _pywintypes_import_error = ex


class ComClient(Client["ComApi"]):
    """
    ComClient to get data from the web

    Returns
    -------
    WebClient
        ComClient instance

    Examples
    -------
    ```python
    with ComClient() as api:
        # use the api here
    ```
    """

    def __init__(self) -> None:
        super().__init__()
        if _win32com_import_error:
            raise _win32com_import_error
        if _pywintypes_import_error:
            raise _pywintypes_import_error
        self.__api: Optional["ComApi"] = None

    def open(self) -> "ComApi":
        if self.__api is None:
            try:
                connection: "Connection" = _client.Dispatch("Macrobond.Connection")
            except com_error as com_ex:

                # raise ValueError(
                #        "Unknown attribute value: " + name + "," + val
                #    ) from ex

                if com_ex.args[1] == "Invalid class string":
                    # TODO: @mb-jp add extra error good here
                    ...
                raise com_ex
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
