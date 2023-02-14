from context import Context
from black_check import black_check
from mypy import mypy
from pylint import pylint
from pycodestyle import pycodestyle
from pdoc3 import pdoc3

import api_code_generator

if __name__ == "__main__":
    Context(api_code_generator.verify, black_check, mypy, pylint, pycodestyle, pdoc3)
