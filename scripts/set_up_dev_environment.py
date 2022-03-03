# -*- coding: utf-8 -*-

from context import Context, PYTHON_36


def set_up_dev_environment(context: Context) -> None:
    python_path = context.get_python_path(PYTHON_36)
    context.shell_command(python_path + " -m pip install --upgrade pip")
    context.shell_command(
        python_path + " -m pip uninstall macrobond_financial", ignore_exit_code=True
    )
    context.shell_command(python_path + " -m pip install -e .[com,web,dev,pandas]")


if __name__ == "__main__":
    Context(set_up_dev_environment)
