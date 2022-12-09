# -*- coding: utf-8 -*-

from context import Context


def build(context: Context) -> None:
    context.python_run(None, "-m build")


if __name__ == "__main__":
    Context(build)
