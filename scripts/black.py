from context import Context


def black(context: Context) -> None:
    context.python_run("black", "--extend-exclude macrobond_data_api_python_env .")


if __name__ == "__main__":
    Context(black)
