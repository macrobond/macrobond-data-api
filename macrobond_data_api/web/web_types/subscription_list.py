from typing import Sequence, TYPE_CHECKING

from dateutil import parser

from .subscription_list_state import SubscriptionListState
from .subscription_list_item import SubscriptionListItem
from .subscription_body import SubscriptionBody

if TYPE_CHECKING:  # pragma: no cover
    from .feed_entities_response import FeedEntitiesResponse


class SubscriptionList(Sequence[SubscriptionListItem], SubscriptionBody):
    __slots__ = ("items",)

    def __init__(self, response: "FeedEntitiesResponse") -> None:
        download_full = response.get("downloadFullListOnOrAfter")
        SubscriptionBody.__init__(
            self,
            parser.parse(response["timeStampForIfModifiedSince"]),
            parser.parse(download_full) if download_full is not None else None,
            SubscriptionListState(response["state"]),
        )
        self.items = list(
            map(
                lambda x: SubscriptionListItem(x["name"], parser.parse(x["modified"])),
                response["entities"],
            )
        )

    def __getitem__(self, index):
        return self.items.__getitem__(index)

    def __len__(self):
        return self.items.__len__()

    def __repr__(self):
        return "SubscriptionList"
