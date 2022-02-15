# -*- coding: utf-8 -*-

from context import Context


def mypy(context: Context) -> None:
    context.install_and_run('mypy', '. --show-error-codes')


if __name__ == "__main__":
    Context(mypy)
