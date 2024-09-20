from typing import Any

import pytest


def test_1(test_values: Any) -> None:
    web = [1, 2, 3]
    com = [1, 2, 3]
    test_values(web, com)
    assert web == com == [1, 2, 3]


def test_2(test_values: Any) -> None:
    web = [1, 2, 3]
    com = [1, 2, 3.000000000000001]
    test_values(web, com)
    assert web == com == [1, 2, 3.000000000000001]


def test_3(test_values: Any) -> None:
    equal = test_values

    equal([0], [0])
    equal([None], [None])


def test_4(test_values: Any) -> None:
    def not_equal(web: Any, com: Any) -> None:
        with pytest.raises(AssertionError):
            test_values(web, com)

    equal = test_values

    # fmt: off
    equal(
        [1.000000000000001],
        [1.000000000000002]
    )
    not_equal(
        [1.00000000000001],
        [1.00000000000002]
    )
    # fmt: on
