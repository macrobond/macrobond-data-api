# -*- coding: utf-8 -*-

from context import Context


def set_up_dev_environment(context: Context) -> None:
    python_path = '"' + context.python_path + '"'
    context.shell_command(python_path + " -m pip install --upgrade pip")
    context.shell_command(
        python_path + " -m pip uninstall macrobond-data-api", ignore_exit_code=True
    )
    context.shell_command(python_path + " -m pip install -e .[dev,extra]")


if __name__ == "__main__":
    Context(set_up_dev_environment)
