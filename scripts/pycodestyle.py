# -*- coding: utf-8 -*-

from context import Context, PYTHON_36


def pycodestyle(context: Context, version_of_python: str = PYTHON_36) -> None:
    python_path = context.get_python_path(version_of_python)
    context.python_run(python_path, "pycodestyle", "--count .")


if __name__ == "__main__":
    Context(pycodestyle)
