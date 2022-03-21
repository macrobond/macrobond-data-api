# # -*- coding: utf-8 -*-
#
# from typing import TYPE_CHECKING
#
# from datetime import datetime
#
# from macrobond_financial.common.api_return_typs import (
#     GetObservationHistoryReturn,
# )
#
# from macrobond_financial.common.typs.series import Series
#
# if TYPE_CHECKING:  # pragma: no cover
#     from macrobond_financial.common.typs.series import SeriesTypedDict
#
#     from ..session import Session
#     from pandas import DataFrame, _typing as pandas_typing  # type: ignore
#
#
# class _GetObservationHistoryReturn(GetObservationHistoryReturn):
#     def __init__(
#         self,
#         session: "Session",
#         serie_name: str,
#         time: datetime,
#         raise_error: bool,
#     ) -> None:
#         super().__init__()
#         self.__session = session
#         self.__serie_name = serie_name
#         self.__time = time
#         self.__raise_error = raise_error
#
#     # def fetch_vintage_series(self) -> "SeriesObservationHistoryResponse":
#     #    response = self.__session.series.fetch_observation_history(
#     #        [self.__serie_name], [self.__time]
#     #    )[0]
#     #
#     #    GetEntitiesError.raise_if(
#     #        self.__raise_error, self.__serie_name, response.get("errorText")
#     #    )
#     #
#     #    return response
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
