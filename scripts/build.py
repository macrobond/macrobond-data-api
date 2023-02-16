from context import run
from code_generation import Verify
from black_check import BlackCheck
from mypy import Mypy
from pylint import Pylint
from pycodestyle import Pycodestyle
from pdoc3 import Pdoc3
from build_tool import BuildTool

if __name__ == "__main__":
    run(Verify, BlackCheck, Mypy, Pylint, Pycodestyle, Pdoc3, BuildTool)
