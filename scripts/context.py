# -*- coding: utf-8 -*-

import os
import importlib.util
import sys
from typing import Callable


class Context:

    hade_error = False

    def __init__(self, *mefs: Callable[['Context'], None]) -> None:
        if mefs is not None:
            if len(mefs) != 0:
                for mef in mefs:
                    mef(self)
                self.test_for_error()

    def shell_command(self, command: str) -> bool:
        print("shell_command :" + command)
        if os.system(command) != 0:
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
        if self.hade_error:
            sys.exit(1)
