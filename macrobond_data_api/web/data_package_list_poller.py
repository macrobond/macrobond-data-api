from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timezone

import time
from typing import List, Optional, Tuple, Union, Callable, TYPE_CHECKING


from .web_api import WebApi
from .web_types.data_package_list_state import DataPackageListState

from .web_types.data_pacakge_list_item import DataPackageListItem
from .web_types.data_package_body import DataPackageBody

if TYPE_CHECKING:
    from macrobond_data_api.web.web_types.data_package_list_context import (
        DataPackageListContext,
        DataPackageListContextManager,
    )


class ExceptionSource(Enum):
    FAILED_TO_BEGIN_FULL_LISTING = 1
    """
    Failed_begin_full_listing can happen after:
        * start()
        * on_exception() 
        * on_full_listing_end()
        * on_incremental_end() 
    """

    FAILED_TO_BEGIN_LISTING = 2
    """
    Failed_begin_listing
        * start()
        * on_exception() 
        * on_full_listing_end()
        * on_incremental_end()
    """

    FAILED_TO_BEGIN_LISTING_INCOMPLETE = 3
    """
    Failed_to_begin_listing_incomplete
        * on_incremental_batch()
    """

    FAILED_TO_GET_BATCH_IN_FULL_LISTING = 4
    """
    Failed_to_get_batch_in_full_listing can happen after:
        * on_full_listing_begin() 
        * on_full_listing_batch() 
    """

    FAILED_TO_GET_BATCH_IN_LISTING = 5
    """
    Failed_to_get_batch_in_listing can happen after:
        * on_incremental_begin() 
        * on_incremental_batch() 
    """

    FAILED_TO_GET_BATCH_IN_LISTING_INCOMPLETE = 6
    """
    Failed_to_get_batch_in_listing_incomplete can happen after:
        * on_incremental_batch()
    """


class DataPackageListPoller(ABC):
    """
    This is work in progress and might change soon.
    Run a loop polling for changed series in the data package list.
    Derive from this class and override `on_full_listing_begin`, `on_full_listing_batch`, `on_full_listing_end`,
    `on_incremental_begin`, `on_incremental_batch` and `on_incremental_end`.

    Parameters
    ----------
    api : WebApi
        The API instance to use.
    download_full_list_on_or_after : datetime, optional
        The saved value of `download_full_list_on_or_after` from the previous run. `None` on first run.
    time_stamp_for_if_modified_since: datetime, optional
        The saved value of `time_stamp_for_if_modified_since` from the previous run. `None`on first run.
    chunk_size : int, optional
        The maximum number of items to include in each on_*_batch()
    """

    def __init__(
        self,
        api: WebApi,
        download_full_list_on_or_after: Optional[datetime] = None,
        time_stamp_for_if_modified_since: Optional[datetime] = None,
        chunk_size: int = 200,
    ) -> None:
        self._api = api
        self._download_full_list_on_or_after = download_full_list_on_or_after
        self._time_stamp_for_if_modified_since = time_stamp_for_if_modified_since
        self._chunk_size = chunk_size

        self.up_to_date_delay = 15 * 60
        """ The time to wait, in seconds, between polls. """
        self.incomplete_delay = 15
        """ The time to wait, in seconds, between continuing partial updates. """
        self.on_error_delay = 30
        """ The time to wait, in seconds, before retrying after an error. """
        self.on_retry_delay = 30

        self._sleep = time.sleep
        self._now = lambda: datetime.now(timezone.utc)
        self._abort = False

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
        This value is used internally to keep track of the the time of the last detected modification.
        Save this value after processing and pass in constructor for the next run.
        """
        return self._time_stamp_for_if_modified_since

    def start(self) -> None:
        """Start processing. It will continue to run until `abort` is called."""
        self._test_access()
        self._abort = False
        while not self._abort:
            if not self._time_stamp_for_if_modified_since or (
                self._download_full_list_on_or_after and self._now() > self._download_full_list_on_or_after
            ):
                sub = self._run_full_listing()
                if sub:
                    self._download_full_list_on_or_after = sub.download_full_list_on_or_after
                    self._time_stamp_for_if_modified_since = sub.time_stamp_for_if_modified_since
            else:
                sub = self._run_listing(self._time_stamp_for_if_modified_since)

                if sub and sub.state != DataPackageListState.UP_TO_DATE:
                    self._sleep(self.incomplete_delay)
                    sub = self._run_listing_incomplete(sub.time_stamp_for_if_modified_since)

                if sub:
                    self._time_stamp_for_if_modified_since = sub.time_stamp_for_if_modified_since

            if self._abort:
                return

            self._sleep(self.up_to_date_delay)

    def _test_access(self) -> None:
        params = {"ifModifiedSince": datetime(3000, 1, 1, tzinfo=timezone.utc).isoformat()}
        response = self._api.session.get("v1/series/getdatapackagelist", params=params)
        if response.status_code == 403:
            raise Exception("Needs access - The account is not set up to use DataPackageList")

    def _run_full_listing(self, max_attempts: int = 3) -> Optional[DataPackageBody]:
        context_manager: Optional["DataPackageListContextManager"] = None
        try:
            context_manager, context, body = self._retry_get_data_package_list_chunked(
                max_attempts, None, ExceptionSource.FAILED_TO_BEGIN_FULL_LISTING
            )
            if context is None or body is None:
                return None

            self.on_full_listing_begin(body)
            if self._abort:
                self.on_full_listing_end(True)
                return None

            if self._try_iterator(
                context,
                body,
                self.on_full_listing_batch,
                self.on_full_listing_end,
                ExceptionSource.FAILED_TO_GET_BATCH_IN_FULL_LISTING,
            ):
                self.on_full_listing_end(False)
                return body
            return None
        finally:
            if context_manager:
                context_manager.__exit__(None, None, None)

    def _run_listing(self, if_modified_since: datetime, max_attempts: int = 3) -> Optional[DataPackageBody]:
        context_manager: Optional["DataPackageListContextManager"] = None
        try:
            context_manager, context, body = self._retry_get_data_package_list_chunked(
                max_attempts, if_modified_since, ExceptionSource.FAILED_TO_BEGIN_LISTING
            )
            if context is None or body is None:
                return None

            self.on_incremental_begin(body)
            if self._abort:
                self.on_incremental_end(True)
                return None

            if (
                self._try_iterator(
                    context,
                    body,
                    self.on_incremental_batch,
                    self.on_incremental_end,
                    ExceptionSource.FAILED_TO_GET_BATCH_IN_LISTING,
                )
                is False
            ):
                return None

            if body.state == DataPackageListState.UP_TO_DATE:
                self.on_incremental_end(False)

            return body
        finally:
            if context_manager:
                context_manager.__exit__(None, None, None)

    def _run_listing_incomplete(self, if_modified_since: datetime, max_attempts: int = 3) -> Optional[DataPackageBody]:
        while True:
            context_manager: Optional["DataPackageListContextManager"] = None
            try:
                context_manager, context, body = self._retry_get_data_package_list_chunked(
                    max_attempts, if_modified_since, ExceptionSource.FAILED_TO_BEGIN_LISTING_INCOMPLETE
                )
                if context is None or body is None:
                    return None

                if (
                    self._try_iterator(
                        context,
                        body,
                        self.on_incremental_batch,
                        self.on_incremental_end,
                        ExceptionSource.FAILED_TO_GET_BATCH_IN_LISTING_INCOMPLETE,
                    )
                    is False
                ):
                    return None

                if body.state == DataPackageListState.UP_TO_DATE:
                    self.on_incremental_end(False)
                    return body

                self._sleep(self.incomplete_delay)

                if_modified_since = body.time_stamp_for_if_modified_since
            finally:
                if context_manager:
                    context_manager.__exit__(None, None, None)

    def _retry_get_data_package_list_chunked(
        self, max_attempts: int, if_modified_since: Optional[datetime], exception_source: ExceptionSource
    ) -> Union[
        Tuple["DataPackageListContextManager", "DataPackageListContext", DataPackageBody],
        Tuple["DataPackageListContextManager", None, None],
    ]:
        attempt = 1
        while True:
            try:
                context_manager = self._api.get_data_package_list_chunked(if_modified_since, self._chunk_size)
                context = context_manager.__enter__()  # pylint: disable=unnecessary-dunder-call
                body = DataPackageBody(
                    context.time_stamp_for_if_modified_since,
                    context.download_full_list_on_or_after,
                    context.state,
                )
                return context_manager, context, body
            except Exception as ex:  # pylint: disable=broad-except
                if attempt > max_attempts:
                    self.on_exception(exception_source, ex)
                    return context_manager, None, None
                self._sleep(self.on_retry_delay * attempt)
                attempt += 1

    def _try_iterator(
        self,
        context: "DataPackageListContext",
        body: DataPackageBody,
        on_batch: Callable[[DataPackageBody, List[DataPackageListItem]], None],
        on_end: Callable[[bool], None],
        exception_source: ExceptionSource,
    ) -> bool:
        iterator = iter(context.items)
        while True:
            try:
                items = [DataPackageListItem(x[0], x[1]) for x in next(iterator)]
            except StopIteration:
                return True
            except Exception as ex:  # pylint: disable=broad-except
                self.on_exception(exception_source, ex)
                return False

            on_batch(body, items)
            if self._abort:
                on_end(True)
                return False

    # full_listing

    @abstractmethod
    def on_full_listing_begin(self, subscription: DataPackageBody) -> None:
        """This override is called when a full listing starts."""

    @abstractmethod
    def on_full_listing_batch(self, subscription: DataPackageBody, items: List[DataPackageListItem]) -> None:
        """This override is called repeatedly with one or more items until all items are listed."""

    @abstractmethod
    def on_full_listing_end(self, is_aborted: bool) -> None:
        """
        This override is called when the full listing is stopped.
        Parameters
        ----------
        is_aborted : bool
            The processing was aborted.
        """

    # listing

    @abstractmethod
    def on_incremental_begin(self, subscription: DataPackageBody) -> None:
        """This override is called when an incremental listing starts."""

    @abstractmethod
    def on_incremental_batch(self, subscription: DataPackageBody, items: List[DataPackageListItem]) -> None:
        """This override is called repeatedly with one or more items until all updated items are listed."""

    @abstractmethod
    def on_incremental_end(self, is_aborted: bool) -> None:
        """
        This override is called when the incremental listing is stopped.
        Parameters
        ----------
        is_aborted : bool
            The processing was aborted.
        """

    @abstractmethod
    def on_exception(self, source: ExceptionSource, exception: Exception) -> None:
        """
        This override is called when the incremental listing is stopped.
        Parameters
        ----------
        exception : Exception
            The exception.
        """

    def abort(self) -> None:
        """
        Call this method to stop processing.
        """
        self._abort = True
