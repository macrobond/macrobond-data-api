from context import Context


def black_check(context: Context) -> None:
    context.python_run("black", "--extend-exclude macrobond_data_api_python_env --check --diff .")


if __name__ == "__main__":
    Context(black_check)
