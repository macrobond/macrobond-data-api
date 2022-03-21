# # -*- coding: utf-8 -*-
#
# from typing import TYPE_CHECKING
#
# from macrobond_financial.common.api_return_typs.get_nth_release_return import (
#     GetNthReleaseReturn,
# )
#
# from macrobond_financial.common.typs.series import Series
#
# if TYPE_CHECKING:  # pragma: no cover
#     from macrobond_financial.common.typs.series import SeriesTypedDict
#     from ..session import Session
#     from pandas import DataFrame, _typing as pandas_typing  # type: ignore
#
#
# class _GetNthReleaseReturn(GetNthReleaseReturn):
#     def __init__(
#         self,
#         session: "Session",
#         serie_name: str,
#         nth: int,
#         raise_error: bool,
#     ) -> None:
#         super().__init__()
#         self.__session = session
#         self.__serie_name = serie_name
#         self.__nth = nth
#         self.__raise_error = raise_error
#
#     def object(self) -> Series:
#         ...
#
#     def dict(self) -> "SeriesTypedDict":
#         ...
#
#     def data_frame(self, *args, **kwargs) -> "DataFrame":
#         ...
#
