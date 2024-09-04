import sys

import pytest

if sys.platform == "win32":
    import winreg  # pylint: disable=E0401


def test_macrobond_config() -> None:
    if sys.platform == "win32":
        sub_key = "Software\\Macrobond Financial\\" + "Communication\\CommunicationState"

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as regkey:
            val = winreg.QueryValueEx(regkey, "PreferredServer")
            assert val[0] in (
                "https://app.macrobondfinancial.com/app",
                "https://app1.macrobondfinancial.com/app",
                "https://app2.macrobondfinancial.com/app",
                "https://app3.macrobondfinancial.com/app",
                "https://app4.macrobondfinancial.com/app",
            ), "Macrobond is not configured to go against the prod environment"
    else:
        pytest.skip('os.name != "nt", this can only run on windows')
