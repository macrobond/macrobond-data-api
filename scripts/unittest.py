# -*- coding: utf-8 -*-

from context import Context, PYTHON_36

UNITTEST_COMMAND = "unittest discover -v -s .\\tests -p **.py"


def unittest(context: Context, version_of_python: str = PYTHON_36) -> None:
    python_path = context.get_python_path(version_of_python)
    context.shell_command(python_path + " -m " + UNITTEST_COMMAND)


if __name__ == "__main__":
    Context(unittest)
