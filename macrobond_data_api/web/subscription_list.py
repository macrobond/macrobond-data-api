import time
from datetime import datetime, timezone, timedelta
from typing import Iterable, List, Dict, Optional

from macrobond_data_api.common.types._parse_iso8601 import _parse_iso8601

from .session import Session

POLL_INTERVAL = timedelta(seconds=15)


class SubscriptionList:
    """
    Class for polling and manipulating subscription lists. Subscription lists can be used to poll for updates at a specific frequency.

    This class shouldn't be instantiated directly, but instead should be retrieved from a web client through `subscription_list`

    Examples
    --------
    ```python
    from datetime import datetime, timezone

    with WebClient() as api:
        subscription_list = api.subscription_list(datetime.now(timezone.utc))
        subscription_list.set(["SEK", "NOK"])
        while True:
            result = subscription_list.poll()
            for key, date in result.items()
                print(f'Series "{key}", last updated "{date}"')
    ```
    """

    _last_poll: Optional[datetime]

    def __init__(self, session: Session, last_modified: datetime):
        self._session = session
        self.last_modified = last_modified
        """
        Stores the date for when the subscription list was last modified.
        """
        self._last_poll = None

    def _call_subscription_list(self, endpoint: str, keys: Iterable[str]) -> None:
        if not isinstance(keys, Iterable):
            raise TypeError("keys is not iterable")
        self._session.post_or_raise(endpoint, json=keys)
        while self._session.post_or_raise("v1/subscriptionlist/check_if_not_included", json=keys).json():
            time.sleep(1)

    def list_subscriptions(self) -> List[str]:
        """
        Lists series currently registered in the subscription list.

        Returns
        -------
        `List[str]`
        """
        return self._session.get_or_raise("v1/subscriptionlist/list").json()

    def set_subscriptions(self, keys: Iterable[str]) -> None:
        """
        Register series to the subscription list. This will erase all previous values in the subscription list.

        .. Important:: This function is not re-entrant!

        Parameters
        ----------
        keys : Iterable[str]
            An iterable of primary keys to register to the subscription list.
        """
        self._call_subscription_list("v1/subscriptionlist/set", keys)

    def add_subscriptions(self, keys: Iterable[str]) -> None:
        """
        Register series to the subscription list. Series that has been registered previously will be kept.

        .. Important:: This function is not re-entrant!

        Parameters
        ----------
        keys : Iterable[str]
            An iterable of primary keys to register to the subscription list.
        """
        self._call_subscription_list("v1/subscriptionlist/add", keys)

    def remove_subscriptions(self, keys: Iterable[str]) -> None:
        """
        Unregister series that has been previously registered to the subscription list.

        .. Important:: This function is not re-entrant!

        Parameters
        ----------
        keys : Iterable[str]
            An iterable of primary keys to unregister from the subscription list.
        """
        self._call_subscription_list("v1/subscriptionlist/remove", keys)

    def poll(self) -> Dict[str, datetime]:
        """
        Polls for any changes on the series in the subscription list.

        Returns
        -------
        Optional[Dict[str, datetime]]
            A dictionary of primary keys that has been updated, and the corresponding last update date.
        """
        interval = (self._last_poll or datetime.now(timezone.utc)) - datetime.now(timezone.utc)
        if interval > timedelta():
            time.sleep(interval.days * 86400 + interval.seconds + interval.microseconds / 1000000)

        data = self._session.get_or_raise(
            "v1/subscriptionlist/get_updates", params={"ifModifiedSince": self.last_modified.isoformat()}
        ).json()
        self._last_poll = datetime.now(timezone.utc) + POLL_INTERVAL
        if data["noMoreChanges"]:
            return {}

        self.last_modified = _parse_iso8601(data["timeStampForIfModifiedSince"])
        return {entity["name"]: _parse_iso8601(entity["modified"]) for entity in data["entities"]}
