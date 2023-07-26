from typing import List, Optional, TypedDict


class SeriesObservationHistoryResponse(TypedDict):
    """The history of changes of an observation"""

    observationDate: str
    """The date of the observation"""

    values: List[Optional[int]]
    """
    The historical values of the observation or an empty list if
    there are no recorded values for the specified date.
    """

    timeStamps: List[Optional[str]]
    """
    A list of timestamps of when the historical values were recorded.
    The first timestamp may be null if the time of the original is unknown.
    """
