# pylint: disable = invalid-name , missing-module-docstring
# mypy: disable_error_code = empty-body

from typing import List, Optional, Literal

from enum import IntEnum

RestrictionLiteral = Literal["url", "email", "date", "positive", "json"]


class MetadataValueType(IntEnum):
    """The type of a metadata value. These values corresponds to the COM VARIANT data types."""

    INT = 3
    """A 32-bit signed integer. VT_I4."""

    DOUBLE = 5
    """A 64-bit floating point number. VT_R8."""

    DATE = 7
    """A date. VT_DATE."""

    STRING = 8
    """A unicode string. VT_BSTR."""

    BOOL = 11
    """A boolean value where -1 is True and 0 is False. VT_BOOL."""


class MetadataValueInformation:
    """Interface for a metadata value in the Macrobond database."""

    @property
    def Value(self) -> object:
        """The value of the metadata."""

    @property
    def Description(self) -> str:
        """The description of the metadata value."""

    @property
    def Comment(self) -> Optional[str]:
        """The comment about the metadata value."""


class MetadataInformation:
    """Interface for a type of metadata in the Macrobond database."""

    @property
    def Name(self) -> str:
        """The name of the metadata."""

    @property
    def Description(self) -> str:
        """The description of the metadata."""

    @property
    def Comment(self) -> str:
        """The comment about the metadata."""

    @property
    def UsesValueList(self) -> bool:
        """Returns True if this type of metadata has a list of possible values."""

    @property
    def ValueType(self) -> MetadataValueType:
        """The datatype that corresponds directly to the COM VT_* values."""

    @property
    def CanHaveMultipleValues(self) -> bool:
        """
        If True then this type of metadata can have multiple
        values in a metadata collection.
        """

    @property
    def IsDatabaseEntity(self) -> bool:
        """
        If True then this type of metadata is an entity that can be retrieved from the database.
        """

    @property
    def CanListValues(self) -> bool:
        """
        If True then the values of this type of metadata can be
        listen using the ListAllValues function.
        """

    @property
    def Restriction(self) -> Optional[RestrictionLiteral]:
        "Potential restriction of the data type. Can be 'date', 'json' or 'positive'."

    def GetValuePresentationText(self, value: object) -> str:
        """Format the value as a text."""

    def GetValueInformation(self, value: object) -> MetadataValueInformation:
        """Get detailed information of a value when this type of metadata uses a list of values."""

    def ListAllValues(self) -> List[MetadataValueInformation]:
        """Get a list of possible values for this type of metadata if it uses a list of values."""

    def ArrangeValues(self, values: object) -> List[object]:
        """Get a list of possible values for this type of metadata if it uses a list of values."""
