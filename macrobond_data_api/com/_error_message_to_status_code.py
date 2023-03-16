from typing import TYPE_CHECKING, Union

from macrobond_data_api.common.enums import StatusCode

if TYPE_CHECKING:  # pragma: no cover
    from .com_types import Entity
    from .com_types import SeriesWithRevisions


def _error_message_to_status_code(entity: Union["Entity", "SeriesWithRevisions"]) -> StatusCode:
    error = entity.ErrorMessage
    if error == "Not found":
        return StatusCode.NOT_FOUND

    return StatusCode.OTHER
