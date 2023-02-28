# pylint: disable=invalid-name, missing-module-docstring
# mypy: disable_error_code = empty-body

from typing import Tuple

from .database import Database


class Connection:
    """Interface for a Macrobond connection."""

    @property
    def Database(self) -> Database:
        """This property returns a reference to the database interface."""

    @property
    def Version(self) -> Tuple[int, int, int]:
        """
        Version	Returns an array of three values for the version of the installed API.
        For example, for the version 1.23.3 it will return [1, 23, 3].
        """

    def Close(self) -> None:
        """
        Free all resources used by the Macrobond API. Opening and closing sessions can be slow,
        so it is usually not a good idea to open and close them for each request
        """
