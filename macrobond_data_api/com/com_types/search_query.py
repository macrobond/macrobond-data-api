# pylint: disable = invalid-name , missing-module-docstring
# mypy: disable_error_code = empty-body


class SearchQuery:
    """Interface for the Macrobond search query."""

    @property
    def Text(self) -> str:
        """The free text search property."""

    @Text.setter
    def Text(self, new_text: str) -> None:
        """The free text search property."""

    @property
    def IncludeDiscontinued(self) -> bool:
        """If to include discontinued series, false by default."""

    @IncludeDiscontinued.setter
    def IncludeDiscontinued(self, new_include_discontinued: bool) -> None:
        """If to include discontinued series, false by default."""

    def SetEntityTypeFilter(self, entity_types: object) -> None:
        """Add an entity type filter."""

    def AddAttributeFilter(self, attribute_name: str, include: bool = True) -> None:
        """Add an attribute filter."""

    def AddAttributeValueFilter(self, attribute_name: str, attribute_values: object, include: bool = True) -> None:
        """Add an attribute value filter."""
