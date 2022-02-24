# -*- coding: utf-8 -*-

import os
from pathlib import Path
import importlib.util
import sys
from typing import Callable, List, Optional

PYTHON_36 = '36'

PYTHON_310 = '310'


class _ShellCommand:

    def __init__(self, command: str, ignore_exit_code: bool, exit_code: int) -> None:
        self.command = command
        self.ignore_exit_code = ignore_exit_code
        self.exit_code = exit_code

    def __str__(self) -> str:
        return f'command: "{self.command}", ignore_exit_code: {self.ignore_exit_code}, ' + \
            f'exit_code: {self.exit_code}'


class Context:

    def __init__(self, *mefs: Callable[['Context'], None]) -> None:
        self.hade_error = False
        self.shell_commands: List[_ShellCommand] = []
        if mefs is not None:
            for mef in mefs:
                mef(self)
            print('--- shell commands ---')
            for shell_command in self.shell_commands:
                print(str(shell_command))

            self.test_for_error()

    def shell_command(self, command: str, ignore_exit_code=False) -> bool:
        print('shell_command start :' + command)
        exit_code = os.system(command)
        print('shell_command end :' + command)
        print('exit_code ' + str(exit_code))
        self.shell_commands.append(_ShellCommand(command, ignore_exit_code, exit_code))
        if exit_code != 0 and not ignore_exit_code:
            self.hade_error = True
            return False
        return True

    def pip_install(self, name: str) -> bool:
        return importlib.util.find_spec(name) is not None or \
            self.shell_command('pip install ' + name)

    def install_and_run(self, name: str, *args: str) -> None:

        if len(args) == 0:
            print("install_and_run :" + name + ' ' + args[0])
        else:
            print("install_and_run :" + name + ' args(' + str(len(args)) + ')')

        if not self.pip_install(name):
            return

        for arg in args:
            self.shell_command(name + ' ' + arg)

    def test_for_error(self) -> None:
        print('Error' if self.hade_error else '')
        if self.hade_error:
            sys.exit(1)

    def get_python_path(self, version_of_python: str = PYTHON_310) -> str:
        python_dir = self.__get_python_path(version_of_python)

        if not os.path.isdir(python_dir):
            self.error_print('Python' + version_of_python + ' not found, ' + python_dir)
            sys.exit(1)

        return f'"{os.path.join(python_dir, "Python")}"'

    def try_get_python_path(self, version_of_python: str = PYTHON_310) -> Optional[str]:
        python_dir = self.__get_python_path(version_of_python)

        isdir = os.path.isdir(python_dir)

        if not isdir:
            self.warning_print('Python' + version_of_python + ' not found, ' + python_dir)

        return f'"{os.path.join(python_dir, "Python")}"' if isdir else None

    def __get_python_path(self, version_of_python: str) -> str:
        return os.path.join(
            Path.home(),
            'AppData',
            'Local',
            'Programs',
            'Python',
            'Python' + version_of_python
        )

    def error_print(self, text: str):
        sys.stderr.write(text)
        sys.stderr.flush()

    def warning_print(self, text: str):
        print('Warning: ' + text)
