# -*- coding: utf-8 -*-

from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .web_types import RevisionHistoryRequest


def create_revision_history_request(
    name: str,
    if_modified_since: datetime = None,
    last_revision: datetime = None,
    last_revision_adjustment: datetime = None,
) -> "RevisionHistoryRequest":
    return {
        "name": name,
        "ifModifiedSince": if_modified_since.isoformat() if if_modified_since else None,
        "lastRevision": last_revision.isoformat() if last_revision else None,
        "lastRevisionAdjustment": last_revision_adjustment.isoformat()
        if last_revision_adjustment
        else None,
    }
