# -*- coding: utf-8 -*-

from context import Context
from mypy import mypy
from pylint import pylint
from pycodestyle import pycodestyle
from pdoc3 import pdoc3
from build_tool import build

if __name__ == "__main__":
    Context(mypy, pylint, pycodestyle, pdoc3, build)
