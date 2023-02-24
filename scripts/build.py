from context import run
from code_generation import Verify
from lint_tools import PyCodeStyle, Pylint, Mypy, BlackCheck
from pdoc3 import Pdoc3
from build_tool import BuildTool

if __name__ == "__main__":
    run(Verify, BlackCheck, Mypy, Pylint, PyCodeStyle, Pdoc3, BuildTool)
