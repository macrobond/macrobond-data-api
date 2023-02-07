# pylint: disable = invalid-name , missing-module-docstring
# mypy: disable_error_code = empty-body

from .metadata import Metadata


class Entity:
    """Interface for a database Macrobond entity."""

    @property
    def Name(self) -> str:
        """The name of the entity."""

    @property
    def PrimaryName(self) -> str:
        """The primary name of the entity."""

    @property
    def IsError(self) -> bool:
        """
        Is true if the request resulted in an error.
        The ErrorMessage property contains the error message.
        """

    @property
    def ErrorMessage(self) -> str:
        """
        The error message if IsError is true.
        Otherwise it is empty.
        """

    @property
    def Title(self) -> str:
        """The title of the entity."""

    @property
    def Metadata(self) -> Metadata:
        """The metadata for the entity."""
