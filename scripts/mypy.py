from context import Context

# https://mypy.readthedocs.io/en/stable/command_line.html


# TODO: @mb-jp use --strict for mypy


def mypy(context: Context) -> None:
    context.python_run(
        "mypy", ". --show-error-codes --exclude macrobond_data_api_python_env --python-version 3.7"
    )


if __name__ == "__main__":
    Context(mypy)
