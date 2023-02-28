from typing import Tuple
import pytest
from macrobond_data_api.com import ComClient, ComClientVersionException


@pytest.mark.parametrize(
    "version",
    [
        (0, 0, 0),  # debug
        (1, 25, 0),
        (2, 0, 0),
    ],
)
def test(version: Tuple[int, int, int]) -> None:
    ComClient._test_version(version)


@pytest.mark.parametrize(
    "version",
    [
        (0, 1, 1),
        (1, 0, 0),
        (1, 24, 0),
    ],
)
def test_error(version: Tuple[int, int, int]) -> None:
    error = "Unsupported version " + (".".join([str(x) for x in version]))
    with pytest.raises(ComClientVersionException, match=error):
        ComClient._test_version(version)
