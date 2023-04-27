import os
from typing import Optional

import pytest

_winreg_import_error: Optional[ImportError] = None
try:
    # winreg is not available on linux so mypy will fail on build server as it is runiong on linux
    from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER  # type: ignore
except ImportError as ex:
    _winreg_import_error = ex


def test_macrobond_config() -> None:
    if os.name != "nt":
        pytest.skip('os.name != "nt", this can only run on windows')

    if _winreg_import_error:
        raise _winreg_import_error

    sub_key = "Software\\Macrobond Financial\\" + "Communication\\CommunicationState"

    with OpenKey(HKEY_CURRENT_USER, sub_key) as regkey:
        val = QueryValueEx(regkey, "PreferredServer")
        assert val[0] in (
            "https://app.macrobondfinancial.com/app",
            "https://app1.macrobondfinancial.com/app",
            "https://app2.macrobondfinancial.com/app",
            "https://app3.macrobondfinancial.com/app",
            "https://app4.macrobondfinancial.com/app",
        ), "Macrobond is not configured to go against the prod environment"
