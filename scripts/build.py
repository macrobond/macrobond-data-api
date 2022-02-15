# -*- coding: utf-8 -*-

from context import Context
from mypy import mypy
from pylint import pylint
from pycodestyle import pycodestyle


def build(context: Context) -> None:
    if not context.pip_install('build'):
        return

    context.shell_command('python -m build')


if __name__ == "__main__":
    Context(mypy, pylint, pycodestyle, build)
