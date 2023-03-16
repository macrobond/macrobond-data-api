from typing import Any, Optional, Dict

from .status_response import StatusResponse


class EntityResponse(StatusResponse):
    """Information about an entity"""

    metadata: Optional[Dict[str, Any]]
    """The metadata of the entity or not specified if there was an error"""
