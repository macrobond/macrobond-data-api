# -*- coding: utf-8 -*-

from context import Context


def pycodestyle(context: Context) -> None:
    context.python_run("pycodestyle", "--count . --exclude=macrobond_data_api_python_env")


if __name__ == "__main__":
    Context(pycodestyle)
