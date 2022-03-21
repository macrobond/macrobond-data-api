# -*- coding: utf-8 -*-

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover

    from pandas import DataFrame, _typing as pandas_typing  # type: ignore

__pandas_Import_error: Optional[ImportError] = None
try:
    import pandas as __pandas  # type: ignore
except ImportError as ex:
    __pandas_Import_error = ex


def _get_pandas() -> "__pandas":
    if __pandas_Import_error:
        raise __pandas_Import_error
    return __pandas
