import asyncio
import sys
from context import run, WorkItem
from code_generation import Verify
from jupyter import JupyterVerify
from test_setup import TestSetup

from pdoc3 import Pdoc3


class Mypy(WorkItem):
    # TODO: @mb-jp use --strict for mypy
    async def run(self) -> None:
        exclude = "--exclude .env --exclude test.py --exclude build --exclude .git"
        args = f". --show-error-codes {exclude} --python-version 3.10"
        await asyncio.gather(
            self.python_run("mypy", args + " --platform win32"),
            self.python_run("mypy", args + " --platform linux"),
        )


class Pylint(WorkItem):
    async def run(self) -> None:
        await self.python_run("pylint", "macrobond_data_api tests -f colorized -r y")


class PyCodeStyle(WorkItem):
    async def run(self) -> None:
        await self.python_run("pycodestyle", "--count . --exclude=.env,test.py,.git")


class Black(WorkItem):
    async def run(self) -> None:
        await self.python_run("black", "--extend-exclude .env,.git .")


class BlackCheck(WorkItem):
    async def run(self) -> None:
        await self.python_run("black", "--extend-exclude .env,.git --check --diff .")


def main() -> None:
    command = sys.argv[1] if len(sys.argv) <= 2 else None

    if command == "--all":
        run(Verify, BlackCheck, Mypy, Pylint, PyCodeStyle, Pdoc3, TestSetup, JupyterVerify, in_sequence=False)

    if command == "--verify":
        run(Verify)

    if command == "--black_check":
        run(BlackCheck)

    if command == "--mypy":
        run(Mypy)

    if command == "--pylint":
        run(Pylint)

    if command == "--py_code_style":
        run(PyCodeStyle)

    if command == "--pdoc3":
        run(Pdoc3)

    if command == "--setup":
        run(TestSetup)

    if command == "--jupyter-verify":
        run(JupyterVerify)

    if command == "--format-code":
        run(Black)

    if command:
        print("bad args " + command)
    else:
        print("no args")

    sys.exit(1)


if __name__ == "__main__":
    main()
