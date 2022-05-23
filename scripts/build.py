# -*- coding: utf-8 -*-

from context import Context
from mypy import mypy
from pylint import pylint
from pycodestyle import pycodestyle


def build(context: Context) -> None:
    context.python_run(None, "-m build")


if __name__ == "__main__":
    Context(mypy, pylint, pycodestyle, build)
