# -*- coding: utf-8 -*-

from context import Context, PYTHON_36

MYPY_COMMAND = "mypy . --show-error-codes"


def mypy(context: Context, version_of_python: str = PYTHON_36) -> None:
    python_path = context.get_python_path(version_of_python)
    context.shell_command(python_path + " -m " + MYPY_COMMAND)


if __name__ == "__main__":
    Context(mypy)
