# -*- coding: utf-8 -*-

from context import Context


def mypy(context: Context) -> None:
    context.python_run("mypy", ". --show-error-codes")


if __name__ == "__main__":
    Context(mypy)
