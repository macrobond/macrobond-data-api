import os
from typing import Optional

import pytest

_winreg_import_error: Optional[ImportError] = None
try:
    # winreg is not available on linux so mypy will fail on build server as it is runiong on linux
    from winreg import OpenKey, QueryValueEx, HKEY_USERS  # type: ignore
except ImportError as ex:
    _winreg_import_error = ex


def test_macrobond_config() -> None:
    if os.name != "nt":
        pytest.skip('os.name != "nt", this can only run on windows')

    if _winreg_import_error:
        raise _winreg_import_error

    sub_key = (
        "S-1-5-21-1109962298-778639869-2696087834-1002\\Software\\Macrobond Financial\\"
        + "Communication\\CommunicationState"
    )

    with OpenKey(HKEY_USERS, sub_key) as regkey:
        val = QueryValueEx(regkey, "PreferredServer")
        assert (
            val[0] == "https://app.macrobondfinancial.com/app"
        ), "Macrobond is not configured to go against the prod environment"