# pylint: disable = invalid-name , missing-module-docstring
# mypy: disable_error_code = empty-body

from typing import Optional, Union, Tuple, Any


class Metadata:
    """Interface for a Macrobond metadata collection."""

    @property
    def IsReadonly(self) -> bool:
        """Gets a value indicating whether this instance is readonly."""

    def GetFirstValue(self, name: str) -> Optional[object]:
        """Get the first metadata value with the specified name."""

    def GetValues(self, name: str) -> Union[Tuple[Any], Tuple]:
        """Get a list of metadata values with the specified name."""

    def ListNames(self) -> Tuple[Tuple[str, str]]:
        """Get a list of metadata names and their descriptions."""

    def AddValue(self, name: str, value: object) -> None:
        """
        Add a value to the metadata collection.
        The value can be a single value or a list of values.
        """

    def HideValue(self, name: str) -> None:
        """Hide a value inherited from a parent metadata collection."""
