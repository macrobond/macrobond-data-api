# -*- coding: utf-8 -*-

from context import Context


def pycodestyle(context: Context) -> None:
    context.install_and_run("pycodestyle", "--count .")


if __name__ == "__main__":
    Context(pycodestyle)
