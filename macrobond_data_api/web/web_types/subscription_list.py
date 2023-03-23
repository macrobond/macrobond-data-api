from dataclasses import dataclass

from typing import List, Sequence, TYPE_CHECKING, overload

from macrobond_data_api.common.types._parse_iso8601 import _parse_iso8601

from .subscription_list_state import SubscriptionListState
from .subscription_list_item import SubscriptionListItem
from .subscription_body import SubscriptionBody

if TYPE_CHECKING:  # pragma: no cover
    from .feed_entities_response import FeedEntitiesResponse


@dataclass(init=False)
class SubscriptionList(Sequence[SubscriptionListItem], SubscriptionBody):
    __slots__ = ("items",)

    items: Sequence[SubscriptionListItem]

    def __init__(self, response: "FeedEntitiesResponse") -> None:
        download_full = response.get("downloadFullListOnOrAfter")
        SubscriptionBody.__init__(
            self,
            _parse_iso8601(response["timeStampForIfModifiedSince"]),
            _parse_iso8601(download_full) if download_full is not None else None,
            SubscriptionListState(response["state"]),
        )
        self.items = [SubscriptionListItem(x["name"], _parse_iso8601(x["modified"])) for x in response["entities"]]

    @overload
    def __getitem__(self, i: int) -> SubscriptionListItem:
        ...

    @overload
    def __getitem__(self, s: slice) -> List[SubscriptionListItem]:
        ...

    def __getitem__(self, key):  # type: ignore
        return self.items[key]

    def __len__(self) -> int:
        return self.items.__len__()
