from context import Context

UNITTEST_COMMAND = "unittest discover -v -s .\\tests -p **.py"


def unittest(context: Context) -> None:
    context.python_run(None, " -m " + UNITTEST_COMMAND)


if __name__ == "__main__":
    Context(unittest)
