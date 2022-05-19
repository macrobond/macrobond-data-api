# -*- coding: utf-8 -*-

from context import Context, PYTHON_36
from mypy import mypy
from pylint import pylint
from pycodestyle import pycodestyle


def build(context: Context, version_of_python: str = PYTHON_36) -> None:
    python_path = context.get_python_path(version_of_python)
    context.shell_command(python_path + " -m build")


if __name__ == "__main__":
    Context(mypy, pylint, pycodestyle, build)
