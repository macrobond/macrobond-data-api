#!/usr/bin/env python3
from dataclasses import dataclass
import importlib.metadata
import os
import platform
import sys
from typing import Optional, List

from macrobond_data_api.util._diagnostic_winreg import _test_regedit_assembly, _test_regedit_username, _test_winreg
from macrobond_data_api.util._common import SaveOutputToFile


@dataclass
class _PackagesInfo:
    exception: Optional[Exception]
    requirement: str
    name: str
    verison: str


# This code is a sin against all people on earth, cooder jesus forgive me.
def _list_packages() -> None:
    try:
        packages_list: List[_PackagesInfo] = []
        requirements = importlib.metadata.requires("macrobond-data-api")
        if requirements is None:
            raise Exception("No requirements found for macrobond-data-api")

        new_model = any(x for x in requirements if x.startswith("keyring "))

        for r in requirements:
            try:
                if new_model:
                    n = r.split(" ")[0]
                else:
                    n = r.split("==")[0]
                    if len(n) > len(r.split(">=")[0]):
                        n = r.split(">=")[0]

                    if len(n) > len(r.split(";")[0]):
                        n = r.split(";")[0]

                if n.endswith("]"):
                    continue

                packages_list.append(_PackagesInfo(None, r, n, importlib.metadata.version(n)))
            except Exception as e:  # pylint: disable=broad-exception-caught
                packages_list.append(_PackagesInfo(e, r, "", ""))

        pad = max(len(f"{p.name} == {p.verison}") for p in packages_list)

        for p in packages_list:
            if p.exception is None:
                print("installed:", f"{p.name} == {p.verison}".ljust(pad), "requirement:", p.requirement)

        for p in packages_list:
            if p.exception is not None:
                print(f"Can't get {p.requirement} version", p.exception)

    except Exception as e:  # pylint: disable=broad-exception-caught
        print("can't get macrobond-data-api depdensys versions", e)


def _print_system_information() -> None:

    print("\n-- System information --\n")

    print("platform.platform():", platform.platform())
    print("sys.platform:", sys.platform)
    print("sys.executable:", sys.executable)
    print("platform.python_compiler():", platform.python_compiler())
    print("platform.python_implementation():", platform.python_implementation())
    print("platform.python_version():", platform.python_version())
    print("platform.architecture():", platform.architecture())

    print("\n-- Python packages info --\n")
    try:
        _list_packages()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print("can't get macrobond-data-api depdensys versions", e)

    print("\n-- macrobond-data-api version --\n")
    try:
        import macrobond_data_api.__version__ as apiInfo  # pylint: disable=import-outside-toplevel

        print("macrobond-data-api version:", apiInfo.__version__)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print("can't get macrobond-data-api version", e)

    print("\n-- keyring info --\n")
    try:
        import keyring  # pylint: disable=import-outside-toplevel

        print("keyring.get_keyring().name:", keyring.get_keyring().name)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print("can't get keyring.get_keyring().name", e)

    print("\n-- Anaconda info --\n")

    print("conda info --verbose")
    print(os.popen("conda info").read())

    # --all is deprecated and will be removed in 24.9. Use --verbose instead.
    print("conda info --all")
    print(os.popen("conda info --all").read())

    if os.name == "nt":

        print("\n-- Windows tests --")

        print("\n-- Test regedit assembly --\n")

        _test_regedit_assembly()

        print("\n-- Test regedit username --\n")

        _test_regedit_username()

        print("\n-- Test ComClient.connection.Version --\n")

        try:
            from macrobond_data_api.com import ComClient  # pylint: disable=import-outside-toplevel

            with ComClient() as api:
                print("Com version:", api.connection.Version)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print("can't get Com version", e)

        print("\n-- Test regedit --\n")

        _test_winreg()


def print_system_information() -> None:
    # fmt: off
    # pylint: disable=line-too-long
    """
    Tests and prints system info, for troubleshooting.
    """
    # pylint: enable=line-too-long
    # fmt: on
    with SaveOutputToFile("system_information"):
        _print_system_information()


if __name__ == "__main__":
    print_system_information()
