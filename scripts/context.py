# -*- coding: utf-8 -*-

import os
import sys
from typing import Callable, List, Optional


def error_print(text: str):
    sys.stderr.write(text)
    sys.stderr.flush()


def warning_print(text: str):
    print("Warning: " + text)


class _ShellCommand:
    def __init__(self, command: str, ignore_exit_code: bool, exit_code: int) -> None:
        self.command = command
        self.ignore_exit_code = ignore_exit_code
        self.exit_code = exit_code

    def __str__(self) -> str:
        return (
            f'command: "{self.command}", ignore_exit_code: {self.ignore_exit_code}, '
            + f"exit_code: {self.exit_code}"
        )


class Context:
    def __init__(self, *mefs: Callable[["Context"], None]) -> None:
        def sys_exit(code: int) -> None:
            sys.exit(code)

        self.hade_error = False
        self.shell_commands: List[_ShellCommand] = []
        self.python_path = sys.executable

        for mef in mefs:
            mef(self)
        print("--- shell commands ---")
        for shell_command in self.shell_commands:
            print(str(shell_command))

        print("Error" if self.hade_error else "")
        if self.hade_error:
            sys_exit(1)

    def shell_command(
        self, command: str, ignore_exit_code=False, prefix: str = ""
    ) -> bool:
        print("shell_command start :" + command)
        exit_code = os.system(prefix + command)
        print("shell_command end :" + command)
        print("exit_code " + str(exit_code))
        self.shell_commands.append(_ShellCommand(command, ignore_exit_code, exit_code))
        if exit_code != 0 and not ignore_exit_code:
            self.hade_error = True
            return False
        return True

    def python_run(
        self, name: Optional[str], *args: str, pip_name: Optional[str] = None
    ) -> None:
        def run(command: str) -> None:
            self.shell_command(command, prefix='"' + self.python_path + '" ')

        if pip_name is None:
            pip_name = name

        if name is not None:
            if pip_name is not None:
                run("-m pip install " + pip_name)

            for arg in args:
                run("-m " + name + " " + arg)
        else:
            for arg in args:
                run(arg)
