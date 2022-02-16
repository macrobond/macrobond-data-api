# -*- coding: utf-8 -*-

from unittest_310 import unittest
from context import Context, PYTHON_36


def unittest_36(context: Context) -> None:
    unittest(context, PYTHON_36)


if __name__ == "__main__":
    Context(unittest_36)
