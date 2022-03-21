# # -*- coding: utf-8 -*-
#
# from typing import TYPE_CHECKING
#
# from datetime import datetime
#
# from macrobond_financial.common.api_return_typs import GetObservationHistoryReturn
#
# from macrobond_financial.common import Series
#
# # from macrobond_financial.common._get_pandas import _get_pandas
#
#
# if TYPE_CHECKING:  # pragma: no cover
#     from ..com_typs import Database
#     from pandas import DataFrame, _typing as pandas_typing  # type: ignore
#
#     from macrobond_financial.common import SeriesTypedDict
#
#
# class _GetObservationHistoryReturn(GetObservationHistoryReturn):
#     def __init__(
#         self,
#         database: "Database",
#         serie_name: str,
#         time: datetime,
#         raise_error: bool,
#     ) -> None:
#         super().__init__()
#         self.__database = database
#         self.__serie_name = serie_name
#         self.__time = time
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
