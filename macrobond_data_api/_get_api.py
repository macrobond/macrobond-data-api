import os
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from macrobond_data_api.common.api import Api

__MACROBOND_DATA_API_CURRENT_API: Optional["Api"] = None


def _get_api() -> "Api":
    global __MACROBOND_DATA_API_CURRENT_API  # pylint: disable= global-statement
    if __MACROBOND_DATA_API_CURRENT_API is not None:
        return __MACROBOND_DATA_API_CURRENT_API

    from macrobond_data_api.web.web_client import (  # pylint: disable=import-outside-toplevel
        WebClient,
        _has_credentials_in_keyring,
    )

    if _has_credentials_in_keyring():
        __MACROBOND_DATA_API_CURRENT_API = WebClient().open()
        return __MACROBOND_DATA_API_CURRENT_API

    if os.name == "nt":
        from macrobond_data_api.com.com_client import (  # pylint: disable=import-outside-toplevel
            ComClient,
        )

        __MACROBOND_DATA_API_CURRENT_API = ComClient().open()
        return __MACROBOND_DATA_API_CURRENT_API

    raise Exception("cant get api")
