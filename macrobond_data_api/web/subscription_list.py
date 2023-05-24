import time
from datetime import datetime, timezone, timedelta
from typing import Sequence, List, Dict

from macrobond_data_api.common.types._parse_iso8601 import _parse_iso8601

from .session import Session


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
        subscription_list.set(['sek', 'nok'])
        while True:
            result = subscription_list.poll()
            for key, date in result.items():
                print(f'Series "{key}", last updated "{date}"')
    ```
    """

    def __init__(self, session: Session, last_modified: datetime, poll_interval: timedelta = timedelta(seconds=15)):
        self._session = session
        self.last_modified = last_modified - timedelta(seconds=5)
        """
        Stores the date for when the subscription list was last modified.
        """

        self.poll_interval = poll_interval
        """
        Specifies the time interval between polls.
        """

        self._next_poll = datetime.now(timezone.utc)

    def list(self) -> List[str]:
        """
        Lists series currently registered in the subscription list.

        Returns
        -------
        `List[str]`
        """
        if not self._session._is_open:
            raise ValueError("WebApi is not open")

        return self._session.get_or_raise("v1/subscriptionlist/list").json()

    def set(self, keys: Sequence[str]) -> None:
        """
        Set what series to include in the subscription list.
        This will replace all previous series in the list.

        .. Important:: You should not make several calls in parallel that modifies the list.

        Parameters
        ----------
        keys : Sequence[str]
            A sequence of series names.
        """
        if not self._session._is_open:
            raise ValueError("WebApi is not open")

        self._call("v1/subscriptionlist/set", keys)

    def add(self, keys: Sequence[str]) -> None:
        """
        Add one or more series to the subscription list.

        .. Important:: You should not make several calls in parallel that modifies the list.

        Parameters
        ----------
        keys : Sequence[str]
            A sequence of series names.
        """
        if not self._session._is_open:
            raise ValueError("WebApi is not open")

        self._call("v1/subscriptionlist/add", keys)

    def remove(self, keys: Sequence[str]) -> None:
        """
        Remove one or more series from the subscription list.

        .. Important:: You should not make several calls in parallel that modifies the list.

        Parameters
        ----------
        keys : Sequence[str]
            A sequence of series names.
        """
        if not self._session._is_open:
            raise ValueError("WebApi is not open")

        key_set = set(keys)
        self._session.post_or_raise("v1/subscriptionlist/remove", json=keys)
        timeout = datetime.now(timezone.utc) + timedelta(minutes=1)
        while (
            datetime.now(timezone.utc) < timeout
            and set(self._session.post_or_raise("v1/subscriptionlist/checkifnotincluded", json=keys).json()) != key_set
        ):
            time.sleep(1)

    def poll(self) -> Dict[str, datetime]:
        """
        Polls for any changes on the series in the subscription list.
        If there are no updates, the method will return an empty list after the poll intervall time. This gives an
        opportinity to abort the polling loop.

        Returns
        -------
        Optional[Dict[str, datetime]]
            A dictionary of primary keys that has been updated, and the corresponding last update date.
        """
        if not self._session._is_open:
            raise ValueError("WebApi is not open")

        interval = self._next_poll - datetime.now(timezone.utc)
        if interval > timedelta():
            time.sleep(interval.total_seconds())

        data = self._session.get_or_raise(
            "v1/subscriptionlist/getupdates", params={"ifModifiedSince": self.last_modified.isoformat()}
        ).json()

        if data["noMoreChanges"]:
            self._next_poll = datetime.now(timezone.utc) + self.poll_interval

        self.last_modified = _parse_iso8601(data["timeStampForIfModifiedSince"])
        return {entity["name"]: _parse_iso8601(entity["modified"]) for entity in data["entities"]}

    def _call(self, endpoint: str, keys: Sequence[str]) -> None:
        if not isinstance(keys, Sequence):
            raise TypeError("keys is not a sequence")
        self._session.post_or_raise(endpoint, json=keys)
        timeout = datetime.now(timezone.utc) + timedelta(minutes=1)
        while (
            datetime.now(timezone.utc) < timeout
            and self._session.post_or_raise("v1/subscriptionlist/checkifnotincluded", json=keys).json()
        ):
            time.sleep(1)
