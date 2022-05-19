# -*- coding: utf-8 -*-

from context import Context, PYTHON_36


def pylint(context: Context, version_of_python: str = PYTHON_36) -> None:
    python_path = context.get_python_path(version_of_python)
    context.python_run(
        python_path, "pylint", " .\\macrobond_financial\\ -f colorized -r y"
    )


if __name__ == "__main__":
    Context(pylint)
