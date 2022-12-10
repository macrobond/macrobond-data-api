# -*- coding: utf-8 -*-

from context import Context


def black(context: Context) -> None:
    context.python_run("black", ".")


if __name__ == "__main__":
    Context(black)
