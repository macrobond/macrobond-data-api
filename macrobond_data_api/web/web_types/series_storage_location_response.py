from typing import TypedDict


class SeriesStorageLocationResponse(TypedDict):
    """Information about a series storage location."""

    name: str
    """The name of the location."""

    seriesPrefix: str
    """The series prefix to use for this location."""
