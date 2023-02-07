# pylint: disable = invalid-name , missing-module-docstring
# mypy: disable_error_code = empty-body

from typing import List

from .entity import Entity


class SearchResult:
    """'Interface for the Macrobond search result."""

    @property
    def Entities(self) -> List[Entity]:
        """The entities returned from search."""

    @property
    def IsTruncated(self) -> bool:
        """A boolean that shows whether the result was too large and is truncated."""
