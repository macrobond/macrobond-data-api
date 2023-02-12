from abc import ABC, abstractmethod
from datetime import datetime, timezone

import time
from typing import List, Optional, cast, TYPE_CHECKING, Callable

from macrobond_data_api.web import WebApi
from .web_types.subscription_list_state import SubscriptionListState

if TYPE_CHECKING:  # pragma: no cover
    from .web_types import SubscriptionBody, SubscriptionListItem


class _AbortException(Exception):
    ...


class SubscriptionListPoller(ABC):
    def __init__(
        self,
        api: WebApi,
        download_full_list_on_or_after: Optional[datetime] = None,
        time_stamp_for_if_modified_since: Optional[datetime] = None,
        _sleep: Callable[[int], None] = time.sleep,
    ) -> None:
        self._api = api
        self._sleep = _sleep
        self._abort = False
        self.up_to_date_delay = 15 * 60
        self.incomplete_delay = 60
        self.on_error_delay = 10
        self._download_full_list_on_or_after = download_full_list_on_or_after
        self._time_stamp_for_if_modified_since = time_stamp_for_if_modified_since

    @property
    def api(self) -> WebApi:
        return self._api

    @property
    def download_full_list_on_or_after(self) -> Optional[datetime]:
        return self._download_full_list_on_or_after

    @property
    def time_stamp_for_if_modified_since(self) -> Optional[datetime]:
        return self._time_stamp_for_if_modified_since

    def start(self) -> None:
        self._abort = False
        while not self._abort:
            if not self._time_stamp_for_if_modified_since or (
                self._download_full_list_on_or_after
                and datetime.now(timezone.utc) > self._download_full_list_on_or_after
            ):
                sub = self._run_full_listing()
                if sub:
                    self._download_full_list_on_or_after = sub.download_full_list_on_or_after
                    self._time_stamp_for_if_modified_since = sub.time_stamp_for_if_modified_since
            else:
                sub = self._run_listing(self._time_stamp_for_if_modified_since)
                if sub:
                    self._time_stamp_for_if_modified_since = sub.time_stamp_for_if_modified_since

            if self._abort:
                return

            self._sleep(self.up_to_date_delay)

    def _run_full_listing(self, max_attempts: int = 3) -> Optional["SubscriptionBody"]:
        is_stated = False

        def _body_callback(body: "SubscriptionBody") -> None:
            is_stated = True  # pylint: disable=unused-variable
            self.on_full_listing_start(body)

        try:
            for attempt in range(1, max_attempts):
                try:
                    sub = self._api.get_subscription_list_iterative(
                        _body_callback,
                        self.on_full_listing_itmes,
                        None,
                    )
                    if not sub:
                        raise ValueError("subscription is None")

                    self.on_full_listing_stop(False, None)
                    return sub
                except Exception as ex:  # pylint: disable=broad-except
                    if self._abort:
                        raise _AbortException() from ex
                    if attempt > max_attempts:
                        raise ex
                    self._sleep(self.on_error_delay)
        except _AbortException as ex:
            if is_stated:
                self.on_listing_stop(True, cast(Exception, ex.__cause__))
        except Exception as ex:  # pylint: disable=broad-except
            if is_stated:
                self.on_listing_stop(False, ex)
        return None

    def _run_listing(self, if_modified_since: datetime, max_attempts: int = 3) -> Optional["SubscriptionBody"]:
        is_stated = False

        def _body_callback(body: "SubscriptionBody") -> None:
            is_stated = True  # pylint: disable=unused-variable
            self.on_listing_start(body)

        try:
            for attempt in range(1, max_attempts):
                try:
                    sub = self._api.get_subscription_list_iterative(
                        _body_callback,
                        self.on_listing_items,
                        if_modified_since,
                    )
                    break
                except Exception as ex:  # pylint: disable=broad-except
                    if self._abort:
                        raise _AbortException() from ex
                    if attempt > max_attempts:
                        raise
                    self._sleep(self.on_error_delay)

            if not sub:
                raise ValueError("subscription is None")

            if sub.state == SubscriptionListState.UP_TO_DATE:
                self.on_listing_stop(False, None)
                return sub

            self._sleep(self.incomplete_delay)

            return self._run_listing_incomplete(sub.time_stamp_for_if_modified_since, is_stated, max_attempts)
        except _AbortException as ex:
            if is_stated:
                self.on_listing_stop(True, cast(Exception, ex.__cause__))
        except Exception as ex:  # pylint: disable=broad-except
            if is_stated:
                self.on_listing_stop(False, ex)
        return None

    def _run_listing_incomplete(
        self, if_modified_since: datetime, is_stated: bool, max_attempts: int = 3
    ) -> Optional["SubscriptionBody"]:
        try:
            while True:
                for attempt in range(1, max_attempts):
                    try:
                        sub = self._api.get_subscription_list_iterative(
                            lambda _: None,
                            self.on_listing_items,
                            if_modified_since,
                        )

                        if not sub:
                            raise ValueError("subscription is None")

                        if sub.state == SubscriptionListState.UP_TO_DATE:
                            self.on_listing_stop(False, None)
                            return sub

                        self._sleep(self.incomplete_delay)

                        if_modified_since = sub.time_stamp_for_if_modified_since
                    except Exception as ex2:  # pylint: disable=broad-except
                        if self._abort:
                            raise _AbortException() from ex2
                        if attempt > max_attempts:
                            raise
                        self._sleep(self.on_error_delay)
        except _AbortException as ex:
            if is_stated:
                self.on_listing_stop(True, cast(Exception, ex.__cause__))
        except Exception as ex:  # pylint: disable=broad-except
            if is_stated:
                self.on_listing_stop(False, ex)
        return None

    # full_listing

    @abstractmethod
    def on_full_listing_start(self, subscription: "SubscriptionBody") -> None:
        ...

    @abstractmethod
    def on_full_listing_itmes(self, subscription: "SubscriptionBody", items: List["SubscriptionListItem"]) -> None:
        ...

    @abstractmethod
    def on_full_listing_stop(self, is_abortd: bool, exception: Optional[Exception]) -> None:
        ...

    # listing

    @abstractmethod
    def on_listing_start(self, subscription: "SubscriptionBody") -> None:
        ...

    @abstractmethod
    def on_listing_items(self, subscription: "SubscriptionBody", items: List["SubscriptionListItem"]) -> None:
        ...

    @abstractmethod
    def on_listing_stop(self, is_abortd: bool, exception: Optional[Exception]) -> None:
        ...

    def abort(self) -> None:
        self._abort = True
