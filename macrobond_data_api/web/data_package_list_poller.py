from abc import ABC, abstractmethod
from datetime import datetime, timezone

import time
from typing import List, Optional, cast, TYPE_CHECKING, Callable

from .web_api import WebApi
from .web_types.data_package_list_state import DataPackageListState

if TYPE_CHECKING:  # pragma: no cover
    from .web_types import DataPackageBody, DataPackageListItem


class _AbortException(Exception):
    pass


class DataPackageListPoller(ABC):
    """
    This is work in progress and might change soon.
    Run a loop polling for changed series in the data package list.
    Derive from this class and override `on_full_listing_start`, `on_full_listing_items`, `on_full_listing_stop`,
    `on_incremental_start`, `on_incremental_items` and `on_incremental_stop`.

    Parameters
    ----------
    api : WebApi
        The API instance to use.
    download_full_list_on_or_after : datetime
        The saved value of `download_full_list_on_or_after` from the previous run. `None` on first run.
    time_stamp_for_if_modified_since: datetime
        The saved value of `time_stamp_for_if_modified_since` from the previous run. `None`on first run.
    """

    def __init__(
        self,
        api: WebApi,
        download_full_list_on_or_after: Optional[datetime] = None,
        time_stamp_for_if_modified_since: Optional[datetime] = None,
        _sleep: Callable[[int], None] = time.sleep,
    ) -> None:
        self.up_to_date_delay = 15 * 60
        """ The time to wait, in seconds, between polls. """
        self.incomplete_delay = 15
        """ The time to wait, in seconds, between continuing partial updates. """
        self.on_error_delay = 30
        """ The time to wait, in seconds, before retrying after an error. """
        self._api = api
        self._sleep = _sleep
        self._abort = False
        self._download_full_list_on_or_after = download_full_list_on_or_after
        self._time_stamp_for_if_modified_since = time_stamp_for_if_modified_since

    @property
    def api(self) -> WebApi:
        return self._api

    @property
    def download_full_list_on_or_after(self) -> Optional[datetime]:
        """
        The time of the scheduled next full listing. Save this value after processing and pass in constructor for
        the next run.
        """
        return self._download_full_list_on_or_after

    @property
    def time_stamp_for_if_modified_since(self) -> Optional[datetime]:
        """
        This value is used internall to keep track of the the time of the last detected modification.
        Save this value after processing and pass in constructor for the next run.
        """
        return self._time_stamp_for_if_modified_since

    def start(self) -> None:
        """Start processing. It will continue to run until `abort` is called."""
        self._test_access()
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

    def _test_access(self) -> None:
        params = {"ifModifiedSince": datetime(3000, 1, 1, tzinfo=timezone.utc)}
        response = self._api.session.get("v1/series/getdatapackagelist", params=params)
        if response.status_code == 403:
            raise Exception("Needs access - The account is not set up to use DataPackageList")

    def _run_full_listing(self, max_attempts: int = 3) -> Optional["DataPackageBody"]:
        is_stated = False

        def _body_callback(body: "DataPackageBody") -> None:
            is_stated = True  # pylint: disable=unused-variable
            self.on_full_listing_start(body)

        try:
            for attempt in range(1, max_attempts):
                try:
                    sub = self._api.get_data_package_list_iterative(
                        _body_callback,
                        self.on_full_listing_items,
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
                self.on_full_listing_stop(True, cast(Exception, ex.__cause__))
        except Exception as ex:  # pylint: disable=broad-except
            if is_stated:
                self.on_full_listing_stop(False, ex)
        return None

    def _run_listing(self, if_modified_since: datetime, max_attempts: int = 3) -> Optional["DataPackageBody"]:
        is_stated = False

        def _body_callback(body: "DataPackageBody") -> None:
            is_stated = True  # pylint: disable=unused-variable
            self.on_incremental_start(body)

        try:
            for attempt in range(1, max_attempts):
                try:
                    sub = self._api.get_data_package_list_iterative(
                        _body_callback,
                        self.on_incremental_items,
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

            if sub.state == DataPackageListState.UP_TO_DATE:
                self.on_incremental_stop(False, None)
                return sub

            self._sleep(self.incomplete_delay)

            return self._run_listing_incomplete(sub.time_stamp_for_if_modified_since, is_stated, max_attempts)
        except _AbortException as ex:
            if is_stated:
                self.on_incremental_stop(True, cast(Exception, ex.__cause__))
        except Exception as ex:  # pylint: disable=broad-except
            if is_stated:
                self.on_incremental_stop(False, ex)
        return None

    def _run_listing_incomplete(
        self, if_modified_since: datetime, is_stated: bool, max_attempts: int = 3
    ) -> Optional["DataPackageBody"]:
        try:
            while True:
                for attempt in range(1, max_attempts):
                    try:
                        sub = self._api.get_data_package_list_iterative(
                            lambda _: None,
                            self.on_incremental_items,
                            if_modified_since,
                        )

                        if not sub:
                            raise ValueError("subscription is None")

                        if sub.state == DataPackageListState.UP_TO_DATE:
                            self.on_incremental_stop(False, None)
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
                self.on_incremental_stop(True, cast(Exception, ex.__cause__))
        except Exception as ex:  # pylint: disable=broad-except
            if is_stated:
                self.on_incremental_stop(False, ex)
        return None

    # full_listing

    @abstractmethod
    def on_full_listing_start(self, subscription: "DataPackageBody") -> None:
        """This override is called when a full listing starts."""

    @abstractmethod
    def on_full_listing_items(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
        """This override is called repeatedly with one or more items until all items are listed."""

    @abstractmethod
    def on_full_listing_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
        """
        This override is called when the full listing is stopped.
        Parameters
        ----------
        is_aborted : bool
            The processing was aborted.
        exception : Optional[Exception]
            If not None, there was an exception.
        """

    # listing

    @abstractmethod
    def on_incremental_start(self, subscription: "DataPackageBody") -> None:
        """This override is called when an incremental listing starts."""

    @abstractmethod
    def on_incremental_items(self, subscription: "DataPackageBody", items: List["DataPackageListItem"]) -> None:
        """This override is called repeatedly with one or more items until all updated items are listed."""

    @abstractmethod
    def on_incremental_stop(self, is_aborted: bool, exception: Optional[Exception]) -> None:
        """
        This override is called when the incremental listing is stopped.
        Parameters
        ----------
        is_aborted : bool
            The processing was aborted.
        exception : Optional[Exception]
            If not None, there was an exception.
        """

    def abort(self) -> None:
        """Call this method to stop processing."""
        self._abort = True
