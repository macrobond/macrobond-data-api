from typing import Optional, List

from .release_event_item import ReleaseEventItem

from .entity_response import EntityResponse


class ReleaseEntityResponse(EntityResponse):

    events: Optional[List[ReleaseEventItem]]
