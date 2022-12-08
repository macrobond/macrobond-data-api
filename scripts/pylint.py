# -*- coding: utf-8 -*-

from context import Context


def pylint(context: Context) -> None:
    context.python_run("pylint", " .\\macrobond_data_api\\ -f colorized -r y")


if __name__ == "__main__":
    Context(pylint)
