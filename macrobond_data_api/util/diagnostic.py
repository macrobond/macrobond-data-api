import importlib.metadata
import os
import platform

try:
    # winreg is not available on linux so mypy will fail on build server as it is runiong on linux
    from winreg import OpenKey, QueryValueEx, HKEY_CLASSES_ROOT, HKEY_CURRENT_USER  # type: ignore
except ImportError:
    pass


def _test_regedit_assembly() -> None:
    sub_key = "CLSID\\{F22A9A5C-E6F2-4FA8-8D1B-E928AB5DDF9B}\\InprocServer32"
    try:
        with OpenKey(HKEY_CLASSES_ROOT, sub_key) as regkey:
            QueryValueEx(regkey, "Assembly")
        print("HKEY_CLASSES_ROOT", sub_key, "is ok")
    except OSError as e:
        print(
            "The Macrobond application is probably not installed.\n"
            + '(Could not find the registry key "HKEY_CLASSES_ROOT\\'
            + sub_key
            + '\\Assembly")\n',
            e,
        )


def _test_regedit_username() -> None:
    sub_key = "Software\\Macrobond Financial\\Communication\\Connector"
    try:
        with OpenKey(HKEY_CURRENT_USER, sub_key) as regkey:
            QueryValueEx(regkey, "UserName")
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


def print_system_information() -> None:

    print("-- system_information --")

    print("Platform information:", platform.platform())
    print("Python compiler:", platform.python_compiler())
    print("Python implementation:", platform.python_implementation())
    print("Python version:", platform.python_version())
    print("Python architecture:", platform.architecture())

    try:
        requirements = importlib.metadata.requires("macrobond-data-api")
        if requirements is None:
            raise Exception("No requirements found for macrobond-data-api")
        for r in requirements:
            try:
                print(r, "installed", importlib.metadata.version(r.split(" ")[0]))
            except Exception as e:  # pylint: disable=broad-exception-caught
                print("can't get versions", e)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print("can't get macrobond-data-api depdensys versions", e)

    try:
        import macrobond_data_api.__version__ as apiInfo  # pylint: disable=import-outside-toplevel

        print("macrobond-data-api version:", apiInfo.__version__)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print("can't get macrobond-data-api version", e)

    try:
        import keyring  # pylint: disable=import-outside-toplevel

        print("keyring.get_keyring().name:", keyring.get_keyring().name)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print("can't get keyring.get_keyring().name", e)

    if os.name == "nt":
        print("-- running on windows --")

        _test_regedit_assembly()

        _test_regedit_username()

        try:
            from macrobond_data_api.com import ComClient  # pylint: disable=import-outside-toplevel

            with ComClient() as api:
                print("Com version:", api.connection.Version)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print("can't get Com version", e)


if __name__ == "__main__":
    print_system_information()
