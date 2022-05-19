# -*- coding: utf-8 -*-

from typing import List, TYPE_CHECKING, Tuple


from macrobond_financial.common.api_return_typs import GetValueInformationReturn

from macrobond_financial.common.typs import MetadataValueInformationItem

from ..session import SessionHttpException

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session


class _GetValueInformationReturn(GetValueInformationReturn):
    def __init__(
        self, session: "Session", name_val: Tuple[Tuple[str, str], ...]
    ) -> None:
        super().__init__(name_val)
        self._session = session

    def object(self) -> List[MetadataValueInformationItem]:
        ret: List[MetadataValueInformationItem] = []
        try:
            for info in self._session.metadata.get_value_information(*self._name_val):
                ret.append(
                    MetadataValueInformationItem(
                        info["attributeName"],
                        info["value"],
                        info["description"],
                        info.get("comment"),
                    )
                )
        except SessionHttpException as ex:
            if ex.status_code == 404:
                raise ValueError(ex.response.json()["detail"]) from ex
            raise ex
        return ret
