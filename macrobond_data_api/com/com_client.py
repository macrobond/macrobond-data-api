import sys

from typing import TYPE_CHECKING, List, Optional, Tuple, cast

from macrobond_data_api.common import Client

from .com_api import ComApi

if TYPE_CHECKING:  # pragma: no cover
    from .com_types import Connection

_win32com_import_error: Optional[ImportError] = None
try:
    from win32com import client as _client
except ImportError as ex:
    _win32com_import_error = ex

_pywintypes_import_error: Optional[ImportError] = None
try:
    from pywintypes import com_error
except ImportError as ex:
    _pywintypes_import_error = ex

try:
    # winreg is not available on linux so mypy will fail on build server as it is runiong on linux
    from winreg import OpenKey, QueryValueEx, HKEY_CLASSES_ROOT, HKEY_CURRENT_USER  # type: ignore
except ImportError:
    pass


def _test_regedit_assembly() -> Optional[str]:
    sub_key = "CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32"
    try:
        with OpenKey(HKEY_CLASSES_ROOT, sub_key) as regkey:
            QueryValueEx(regkey, "Assembly")
    except OSError:
        return (
            "The Macrobond application is probably not installed.\n"
            + '(Could not find the registry key "HKEY_CLASSES_ROOT\\'
            + sub_key
            + '\\Assembly")\n'
        )
    return None


def _test_regedit_username() -> Optional[str]:
    sub_key = "Software\\Macrobond Financial\\Communication\\Connector"
    try:
        with OpenKey(HKEY_CURRENT_USER, sub_key) as regkey:
            QueryValueEx(regkey, "UserName")
    except OSError:
        return (
            "The Macrobond application does not seem to be logged in. Please start the application and verify that "
            + "it works properly.\n"
            + '(Could not find the registry key "HKEY_CURRENT_USER\\'
            + sub_key
            + '\\UserName")\n'
        )
    return None


class ComClientVersionException(Exception):
    pass


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
        self.has_closed = False
        self.__api: Optional["ComApi"] = None

    @property
    def is_open(self) -> bool:
        return bool(self.__api)

    def open(self) -> "ComApi":
        error_hints: List[str] = []
        try:
            return self.open_and_hint(error_hints)
        except Exception:
            if len(error_hints) != 0:
                print("\n\nERROR in ComClient.open()", file=sys.stderr)

            for hint in error_hints:
                print("\n" + hint, file=sys.stderr)

            if len(error_hints) != 0:
                print("", file=sys.stderr)

            raise

    def open_and_hint(self, hints: List[str]) -> "ComApi":
        if self.has_closed:
            raise ValueError("ComClient cannot be reopend")

        if _win32com_import_error:
            raise _win32com_import_error

        if _pywintypes_import_error:
            raise _pywintypes_import_error

        if self.__api is None:
            try:
                connection: "Connection" = cast("Connection", _client.Dispatch("Macrobond.Connection"))
            except com_error:
                new_hint = _test_regedit_assembly()
                if new_hint:
                    hints.append(new_hint)

                new_hint = _test_regedit_username()
                if new_hint:
                    hints.append(new_hint)
                raise

            version = connection.Version
            ComClient._test_version(version)

            self.__api = ComApi(connection, version)
        return self.__api

    @staticmethod
    def _test_version(version: Tuple[int, int, int]) -> None:
        if version == (0, 0, 0):
            return

        if version >= (1, 25, 0):
            return

        raise ComClientVersionException("Unsupported version " + (".".join([str(x) for x in version])))

    def close(self) -> None:
        """
        free all resources used by the Macrobond API.
        Opening and closing sessions can be slow,
        so it is usually not a good idea to open and close them for each request
        """
        self.has_closed = True
        if self.__api:
            self.__api._metadata_type_directory.close()
            self.__api.connection.Close()
            self.__api._connection = None
            self.__api = None
