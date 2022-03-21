# # -*- coding: utf-8 -*-
#
# from typing import TYPE_CHECKING
#
#
# from macrobond_financial.common.api_return_typs import GetNthReleaseReturn
#
# from macrobond_financial.common import Series
#
# # from macrobond_financial.common._get_pandas import _get_pandas
#
#
# if TYPE_CHECKING:  # pragma: no cover
#     from ..com_typs import Database, Series as ComSeries
#     from pandas import DataFrame, _typing as pandas_typing  # type: ignore
#
#     from macrobond_financial.common import SeriesTypedDict
#
#
# class _GetNthReleaseReturn(GetNthReleaseReturn):
#     def __init__(
#         self,
#         database: "Database",
#         serie_name: str,
#         nth: int,
#         raise_error: bool,
#     ) -> None:
#         super().__init__()
#         self.__database = database
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
