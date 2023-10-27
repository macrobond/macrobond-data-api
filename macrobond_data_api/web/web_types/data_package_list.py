from dataclasses import dataclass

from typing import List, Sequence, TYPE_CHECKING, overload

from macrobond_data_api.common.types._parse_iso8601 import _parse_iso8601

from .data_package_list_state import DataPackageListState
from .data_pacakge_list_item import DataPackageListItem
from .data_package_body import DataPackageBody

if TYPE_CHECKING:  # pragma: no cover
    from .feed_entities_response import FeedEntitiesResponse


@dataclass(init=False)
class DataPackageList(Sequence[DataPackageListItem], DataPackageBody):
    __slots__ = ("items",)

    items: Sequence[DataPackageListItem]

    def __init__(self, response: "FeedEntitiesResponse") -> None:
        download_full = response.get("downloadFullListOnOrAfter")
        DataPackageBody.__init__(
            self,
            _parse_iso8601(response["timeStampForIfModifiedSince"]),
            _parse_iso8601(download_full) if download_full is not None else None,
            DataPackageListState(response["state"]),
        )
        self.items = [DataPackageListItem(x["name"], _parse_iso8601(x["modified"])) for x in response["entities"]]

    @overload
    def __getitem__(self, i: int) -> DataPackageListItem:
        pass

    @overload
    def __getitem__(self, s: slice) -> List[DataPackageListItem]:
        pass

    def __getitem__(self, key):  # type: ignore
        return self.items[key]

    def __len__(self) -> int:
        return self.items.__len__()
