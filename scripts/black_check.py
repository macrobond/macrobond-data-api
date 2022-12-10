# -*- coding: utf-8 -*-

from context import Context


def black_check(context: Context) -> None:
    context.python_run("black", "--check .")


if __name__ == "__main__":
    Context(black_check)
