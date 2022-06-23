# -*- coding: utf-8 -*-

from typing import Optional

_pandas_import_error: Optional[ImportError] = None
try:
    import pandas as _pandas  # type: ignore
except ImportError as ex:
    _pandas_import_error = ex


def _get_pandas() -> "_pandas":
    if _pandas_import_error:
        raise _pandas_import_error
    return _pandas
