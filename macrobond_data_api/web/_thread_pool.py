import os
from concurrent.futures import (
    wait,
    Future,
    FIRST_COMPLETED,
    as_completed,
    ThreadPoolExecutor,
)
from typing import Callable, Generic, TypeVar, Set, cast

TypeVarOut = TypeVar("TypeVarOut")


class _ThreadPool(Generic[TypeVarOut]):
    def __init__(
        self,
        done_callback: Callable[[TypeVarOut], None],
        max_workers: int = None,
    ) -> None:

        if max_workers is None:
            max_workers = os.cpu_count() or 1
        if max_workers <= 0:
            raise ValueError("max_workers must be greater than 0")

        self._max_workers = cast(int, max_workers)
        self._done_callback = done_callback
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._items: Set[Future] = set()

    def submit(self, *args, **kwargs) -> None:
        self._items.add(self._executor.submit(*args, **kwargs))
        timeout = None if len(self._items) == self._max_workers else 0
        wait_result = wait(
            self._items,
            return_when=FIRST_COMPLETED,
            timeout=timeout,
        )
        self._items = wait_result.not_done
        for done in wait_result.done:
            self._done_callback(done.result())

    def __enter__(self) -> "_ThreadPool":
        self._executor = self._executor.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        try:
            for done in as_completed(self._items):
                self._done_callback(done.result())
            self._items = set()
        finally:
            self._executor.__exit__(None, None, None)
