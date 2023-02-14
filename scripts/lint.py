from context import Context
from api_code_generator import verify
from black_check import black_check
from mypy import mypy
from pylint import pylint
from pycodestyle import pycodestyle
from pdoc3 import pdoc3

if __name__ == "__main__":
    Context(verify, black_check, mypy, pylint, pycodestyle, pdoc3)
