import os
import sys
from dataclasses import dataclass
from typing import List, Any, Optional, Literal

if sys.platform == "win32":
    import winreg  # pylint: disable=E0401
else:
    winreg: Any = None


# Not in use in this file
def _test_regedit_assembly() -> None:
    sub_key = "CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32"
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, sub_key, 0, winreg.KEY_READ) as regkey:
            winreg.QueryValueEx(regkey, "Assembly")
        print("HKEY_CLASSES_ROOT", sub_key, "is ok")
    except OSError as e:
        print(
            "The Macrobond application is probably not installed.\n"
            + '(Could not find the registry key "HKEY_CLASSES_ROOT\\'
            + sub_key
            + '\\Assembly")\n',
            e,
        )


# Not in use in this file
def _test_regedit_username() -> None:
    sub_key = "Software\\Macrobond Financial\\Communication\\Connector"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as regkey:
            winreg.QueryValueEx(regkey, "UserName")
        print("HKEY_CURRENT_USER", sub_key, "is ok")
    except OSError as e:
        print(
            "The Macrobond application does not seem to be logged in. Please start the application and verify that "
            + "it works properly.\n"
            + '(Could not find the registry key "HKEY_CURRENT_USER\\'
            + sub_key
            + '\\UserName")\n',
            e,
        )


@dataclass
class _KeyData:
    key_type_name: str
    key: str
    name: str
    data_type: int
    data: Any

    @property
    def is_file(self) -> bool:
        return self.data_type == 1 and isinstance(self.data, str) and self.data.startswith("file:///")

    @property
    def file_path(self) -> str:
        if self.is_file:
            return self.data[8:]
        raise ValueError("Not a file")

    def file_exists(self) -> bool:
        if self.is_file:
            return os.path.isfile(self.file_path)
        raise ValueError("Not a file")

    def test_is_same_key(self, key: "_KeyData") -> bool:
        return self.key_type_name == key.key_type_name and self.key == key.key and self.name == key.name

    def test_is_same_data(self, key: "_KeyData") -> bool:
        return self.data_type == key.data_type and self.data == key.data

    @staticmethod
    def get_key_type_name(key_type: int) -> str:
        if key_type == winreg.HKEY_CLASSES_ROOT:
            return "HKEY_CLASSES_ROOT"
        if key_type == winreg.HKEY_CURRENT_USER:
            return "HKEY_CURRENT_USER"
        if key_type == winreg.HKEY_LOCAL_MACHINE:
            return "HKEY_LOCAL_MACHINE"

        raise ValueError("Invalid key type")

    @classmethod
    def list_kyes_classes_root(cls, sub_key: str) -> List["_KeyData"]:
        return cls.list_kyes(winreg.HKEY_CLASSES_ROOT, sub_key)

    @classmethod
    def list_kyes_local_machine(cls, sub_key: str) -> List["_KeyData"]:
        return cls.list_kyes(winreg.HKEY_LOCAL_MACHINE, sub_key)

    @classmethod
    def list_kyes_current_user(cls, sub_key: str) -> List["_KeyData"]:
        return cls.list_kyes(winreg.HKEY_CURRENT_USER, sub_key)

    @classmethod
    def list_kyes(
        cls, key_type: int, sub_key: str, ret: List["_KeyData"] = None, key_type_name: str = None
    ) -> List["_KeyData"]:
        if ret is None:
            ret = []
        if key_type_name is None:
            key_type_name = cls.get_key_type_name(key_type)

        hkey = None
        try:
            hkey = winreg.OpenKey(key_type, sub_key, 0, winreg.KEY_READ)
            i = 0
            try:
                while 1:
                    n, v, t = winreg.EnumValue(hkey, i)
                    ret.append(_KeyData(key_type_name, sub_key, n, t, v))
                    i += 1
            except OSError:
                pass

            i = 0
            while True:
                try:
                    ret = cls.list_kyes(key_type, sub_key + "\\" + winreg.EnumKey(hkey, i), ret)
                    i += 1
                except OSError:
                    break
        except FileNotFoundError:
            pass
        finally:
            if hkey is not None:
                winreg.CloseKey(hkey)
        return ret

    def verify(self, context: "_TestWinregContext", actual: "_KeyData") -> None:
        print(actual.key_type_name, actual.key, actual.name, actual.data_type, actual.data)

        if not actual.test_is_same_data(self):
            context.mismatch_list.append(_Error(actual, self))


@dataclass
class _TestKeyData(_KeyData):

    mode: Literal["file", "fileUrl", "ignore_data", "pass"]

    def verify(self, context: "_TestWinregContext", actual: "_KeyData") -> None:

        if self.mode == "pass":
            print(actual.key_type_name, actual.key, actual.name, actual.data_type, "")
            return

        print(actual.key_type_name, actual.key, actual.name, actual.data_type, actual.data)

        if self.mode == "ignore_data":
            return

        if self.mode == "file":
            path: str = actual.data
            if actual.data.startswith('"'):
                path = path[1:-1]
            if not os.path.isfile(path):
                context.file_missing.append(_Error(actual, self))
        elif self.mode == "fileUrl":
            if not actual.is_file or not actual.file_exists():
                context.file_missing.append(_Error(actual, self))
        else:
            raise ValueError("Invalid mode")


@dataclass
class _Error:
    actual: "_KeyData"
    expected: Optional["_KeyData"]


class _TestWinregContext:
    mismatch_list: List["_Error"] = []
    missing_list: List["_KeyData"] = []
    file_missing: List["_Error"] = []

    def verify_kyes_classes_root(self, sub_key: str, expected_list: List["_KeyData"]) -> None:
        self.verify_kyes(winreg.HKEY_CLASSES_ROOT, sub_key, expected_list)

    def verify_kyes_local_machine(self, sub_key: str, expected_list: List["_KeyData"]) -> None:
        self.verify_kyes(winreg.HKEY_LOCAL_MACHINE, sub_key, expected_list)

    def verify_kyes_current_user(self, sub_key: str, expected_list: List["_KeyData"]) -> None:
        self.verify_kyes(winreg.HKEY_CURRENT_USER, sub_key, expected_list)

    def verify_kyes(self, key_type: int, sub_key: str, expected_list: List["_KeyData"]) -> None:
        print("\n-- Verifying --", _KeyData.get_key_type_name(key_type) + "\\" + sub_key, "--")

        actual_list = _KeyData.list_kyes(key_type, sub_key)

        # print(actual_list, "\n")

        for actual in actual_list:
            try:
                expected = next(filter(lambda x: x.test_is_same_key(actual), expected_list))  # pylint: disable=w0640
                expected.verify(self, actual)
                expected_list.remove(expected)
            except StopIteration:
                print(actual.key_type_name, actual.key, actual.name, actual.data_type, actual.data)

                if actual.is_file and not actual.file_exists():
                    self.file_missing.append(_Error(actual, None))

        for expected in expected_list:
            self.missing_list.append(expected)


def _test_winreg() -> None:

    context = _TestWinregContext()

    # macrobond
    expected_list = [
        _KeyData(
            key_type_name="HKEY_CLASSES_ROOT", key="macrobond", name="", data_type=1, data="URL:Macrobond Protocol"
        ),
        _KeyData(key_type_name="HKEY_CLASSES_ROOT", key="macrobond", name="URL Protocol", data_type=1, data=""),
        _TestKeyData(
            key_type_name="HKEY_CLASSES_ROOT",
            key="macrobond\\DefaultIcon",
            name="",
            data_type=1,
            data='"C:\\Program Files\\Macrobond Financial\\Macrobond\\MacroBond.exe"',
            mode="file",
        ),
        _TestKeyData(
            key_type_name="HKEY_CLASSES_ROOT",
            key="macrobond\\shell\\open\\command",
            name="",
            data_type=1,
            data='"C:\\Program Files\\Macrobond Financial\\Macrobond\\MacroBond.exe" "%1"',
            mode="ignore_data",
        ),
    ]
    context.verify_kyes_classes_root(r"macrobond", expected_list)

    # Macrobond.Connection
    expected_list = [
        _KeyData(
            key_type_name="HKEY_CLASSES_ROOT",
            key="Macrobond.Connection",
            name="",
            data_type=1,
            data="Abacus.ComApi.Connection",
        ),
        _KeyData(
            key_type_name="HKEY_CLASSES_ROOT",
            key="Macrobond.Connection\\CLSID",
            name="",
            data_type=1,
            data="{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}",
        ),
    ]
    context.verify_kyes_classes_root(r"Macrobond.Connection", expected_list)

    # WOW6432Node\CLSID\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}
    expected_list = [
        _KeyData(
            key_type_name="HKEY_CLASSES_ROOT",
            key="WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}",
            name="",
            data_type=1,
            data="Macrobond COM API",
        ),
        _KeyData(
            key_type_name="HKEY_CLASSES_ROOT",
            key="WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\Implemented Categories\\{62C8FE65-4EBB-45e7-B440-6E39B2CDBF29}",
            name="",
            data_type=1,
            data="",
        ),
        _KeyData(
            key_type_name="HKEY_CLASSES_ROOT",
            key="WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="",
            data_type=1,
            data="mscoree.dll",
        ),
        _KeyData(
            key_type_name="HKEY_CLASSES_ROOT",
            key="WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="ThreadingModel",
            data_type=1,
            data="Both",
        ),
        _KeyData(
            key_type_name="HKEY_CLASSES_ROOT",
            key="WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="Class",
            data_type=1,
            data="Abacus.ComApi.Connection",
        ),
        _KeyData(
            key_type_name="HKEY_CLASSES_ROOT",
            key="WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="Assembly",
            data_type=1,
            data="Abacus.ComApi, Version=1.28.104.16110, Culture=neutral, PublicKeyToken=109bd21c6ab0cfcd",
        ),
        _KeyData(
            key_type_name="HKEY_CLASSES_ROOT",
            key="WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="RuntimeVersion",
            data_type=1,
            data="v4.0.30319",
        ),
        _KeyData(
            key_type_name="HKEY_CLASSES_ROOT",
            key="WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="CodeBase",
            data_type=1,
            data="file:///C:\\Program Files\\Macrobond Financial\\Macrobond\\Abacus.ComApi.dll",
        ),
        _KeyData(
            key_type_name="HKEY_CLASSES_ROOT",
            key="WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\ProgID",
            name="",
            data_type=1,
            data="Macrobond.Connection",
        ),
    ]
    context.verify_kyes_classes_root(r"WOW6432Node\CLSID\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}", expected_list)

    # SOFTWARE\Classes\Macrobond.Connection
    expected_list = [
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\Macrobond.Connection",
            name="",
            data_type=1,
            data="Abacus.ComApi.Connection",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\Macrobond.Connection\\CLSID",
            name="",
            data_type=1,
            data="{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}",
        ),
    ]
    context.verify_kyes_local_machine(r"SOFTWARE\Classes\Macrobond.Connection", expected_list)

    # SOFTWARE\Classes\CLSID\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}
    expected_list = [
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}",
            name="",
            data_type=1,
            data="Macrobond COM API",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\Implemented Categories\\{62C8FE65-4EBB-45e7-B440-6E39B2CDBF29}",
            name="",
            data_type=1,
            data="",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="",
            data_type=1,
            data="mscoree.dll",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="ThreadingModel",
            data_type=1,
            data="Both",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="Class",
            data_type=1,
            data="Abacus.ComApi.Connection",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="Assembly",
            data_type=1,
            data="Abacus.ComApi, Version=1.28.104.16110, Culture=neutral, PublicKeyToken=109bd21c6ab0cfcd",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="RuntimeVersion",
            data_type=1,
            data="v4.0.30319",
        ),
        _TestKeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="CodeBase",
            data_type=1,
            data="file:///C:\\Program Files\\Macrobond Financial\\Macrobond\\Abacus.ComApi.dll",
            mode="fileUrl",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\ProgID",
            name="",
            data_type=1,
            data="Macrobond.Connection",
        ),
    ]
    context.verify_kyes_local_machine(r"SOFTWARE\Classes\CLSID\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}", expected_list)

    # SOFTWARE\Classes\WOW6432Node\CLSID\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}
    expected_list = [
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}",
            name="",
            data_type=1,
            data="Macrobond COM API",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\Implemented Categories\\{62C8FE65-4EBB-45e7-B440-6E39B2CDBF29}",
            name="",
            data_type=1,
            data="",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="",
            data_type=1,
            data="mscoree.dll",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="ThreadingModel",
            data_type=1,
            data="Both",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="Class",
            data_type=1,
            data="Abacus.ComApi.Connection",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="Assembly",
            data_type=1,
            data="Abacus.ComApi, Version=1.28.104.16110, Culture=neutral, PublicKeyToken=109bd21c6ab0cfcd",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="RuntimeVersion",
            data_type=1,
            data="v4.0.30319",
        ),
        _TestKeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="CodeBase",
            data_type=1,
            data="file:///C:\\Program Files\\Macrobond Financial\\Macrobond\\Abacus.ComApi.dll",
            mode="fileUrl",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\Classes\\WOW6432Node\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\ProgID",
            name="",
            data_type=1,
            data="Macrobond.Connection",
        ),
    ]
    context.verify_kyes_local_machine(
        r"SOFTWARE\Classes\WOW6432Node\CLSID\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}", expected_list
    )

    # SOFTWARE\WOW6432Node\Classes\CLSID\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}
    expected_list = [
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\WOW6432Node\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}",
            name="",
            data_type=1,
            data="Macrobond COM API",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\WOW6432Node\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\Implemented Categories\\{62C8FE65-4EBB-45e7-B440-6E39B2CDBF29}",
            name="",
            data_type=1,
            data="",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\WOW6432Node\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="",
            data_type=1,
            data="mscoree.dll",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\WOW6432Node\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="ThreadingModel",
            data_type=1,
            data="Both",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\WOW6432Node\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="Class",
            data_type=1,
            data="Abacus.ComApi.Connection",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\WOW6432Node\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="Assembly",
            data_type=1,
            data="Abacus.ComApi, Version=1.28.104.16110, Culture=neutral, PublicKeyToken=109bd21c6ab0cfcd",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\WOW6432Node\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="RuntimeVersion",
            data_type=1,
            data="v4.0.30319",
        ),
        _TestKeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\WOW6432Node\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32",
            name="CodeBase",
            data_type=1,
            data="file:///C:\\Program Files\\Macrobond Financial\\Macrobond\\Abacus.ComApi.dll",
            mode="fileUrl",
        ),
        _KeyData(
            key_type_name="HKEY_LOCAL_MACHINE",
            key="SOFTWARE\\WOW6432Node\\Classes\\CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\ProgID",
            name="",
            data_type=1,
            data="Macrobond.Connection",
        ),
    ]
    context.verify_kyes_local_machine(
        r"SOFTWARE\WOW6432Node\Classes\CLSID\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}", expected_list
    )

    # Software\Macrobond Financial\Communication
    expected_list = [
        _KeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\CommunicationState",
            name="PreferredServer",
            data_type=1,
            data="https://app1.macrobondfinancial.com/app",
        ),
        _KeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\CommunicationState",
            name="Department",
            data_type=1,
            data="",
        ),
        _KeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\CommunicationState",
            name="ServerList",
            data_type=7,
            data=[
                "https://app1.macrobondfinancial.com/app",
                "https://app2.macrobondfinancial.com/app",
                "https://app3.macrobondfinancial.com/app",
            ],
        ),
        _KeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\CommunicationState",
            name="UserRoles",
            data_type=7,
            data=["client", "fat_client"],
        ),
        _KeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\CommunicationState",
            name="UserGroups",
            data_type=7,
            data=[],
        ),
        _KeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\CommunicationState",
            name="EscapedServiceName",
            data_type=1,
            data="mapp",
        ),
        _TestKeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\Connector",
            name="UserName",
            data_type=1,
            data="",
            mode="ignore_data",
        ),
        _TestKeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\Connector",
            name="Password",
            data_type=1,
            data="",
            mode="pass",
        ),
        _KeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\Connector",
            name="ProxyUsage",
            data_type=4,
            data=0,
        ),
        _KeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\Connector",
            name="ProxyServerAddress",
            data_type=1,
            data="",
        ),
        _KeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\Connector",
            name="ProxyUserName",
            data_type=1,
            data="",
        ),
        _TestKeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\Connector",
            name="ProxyPassword",
            data_type=1,
            data="",
            mode="pass",
        ),
        _KeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\Connector",
            name="UseWindowsCredentials",
            data_type=4,
            data=1,
        ),
        _KeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\Connector",
            name="DefaultServer",
            data_type=1,
            data="https://app1.macrobondfinancial.com/app",
        ),
        _KeyData(
            key_type_name="HKEY_CURRENT_USER",
            key="Software\\Macrobond Financial\\Communication\\Role",
            name="Role",
            data_type=1,
            data="macrobond internal 2020",
        ),
    ]
    context.verify_kyes_current_user(r"Software\Macrobond Financial\Communication", expected_list)

    print("\n\n-- Mismatch:", len(context.mismatch_list), "--")
    for error in context.mismatch_list:
        print("actual: ", error.actual)
        if error.expected is not None:
            print("expected: ", error.expected)
        print()

    print("\n\n-- Missing:", len(context.missing_list), "--")
    for key in context.missing_list:
        print(key)
        print()

    print("\n\n-- File missing:", len(context.file_missing), "--")
    for error in context.file_missing:
        print("actual: ", error.actual)
        if error.expected is not None:
            print("expected: ", error.expected)
        print()


if __name__ == "__main__":
    _test_winreg()
