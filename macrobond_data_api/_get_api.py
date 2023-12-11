import os
import sys
from typing import TYPE_CHECKING, Optional, List


if TYPE_CHECKING:
    from macrobond_data_api.common.api import Api

__MACROBOND_DATA_API_CURRENT_API: Optional["Api"] = None


def _get_api() -> "Api":
    global __MACROBOND_DATA_API_CURRENT_API  # pylint: disable= global-statement
    if __MACROBOND_DATA_API_CURRENT_API:
        return __MACROBOND_DATA_API_CURRENT_API

    hints: List[str] = []

    try:
        from macrobond_data_api.web.web_client import (  # pylint: disable=import-outside-toplevel
            WebClient,
            _has_credentials_in_keyring,
        )

        if _has_credentials_in_keyring():
            hints.append("Trying to open a WebClient.")
            try:
                __MACROBOND_DATA_API_CURRENT_API = WebClient().open()
                return __MACROBOND_DATA_API_CURRENT_API
            except Exception:
                hints.append("Failed to open a WebClient.")
                raise
        hints.append(
            "Did not find any Key in the keyring, so we can not use the WebClient.\n"
            + 'If you want to use the WebClient, try runing the "save_credentials_to_keyring()" learn more: '
            + "https://github.com/macrobond/macrobond-data-api#using-of-system-keyring\n"
            + "or create an instance of the WebClient by passing the credentials as parameters."
        )

        if os.name == "nt":
            from macrobond_data_api.com.com_client import (  # pylint: disable=import-outside-toplevel
                ComClient,
            )

            hints.append("Trying to open a ComClient.")
            try:
                __MACROBOND_DATA_API_CURRENT_API = ComClient().open_and_hint(hints)
                return __MACROBOND_DATA_API_CURRENT_API
            except Exception:
                hints.append("Failed to open a ComClient.")
                raise
        else:
            hints.append("This system is not running Windows, so we can not use the ComClient.")

        hints.append("Did not find any suitable client to use.")

        raise Exception("Did not find any suitable client to use.")

    except Exception:
        for e in hints:
            print("\n" + str(e), file=sys.stderr)
        print("", file=sys.stderr)

        raise
