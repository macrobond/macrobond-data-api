import os
from unittest import UNITTEST_COMMAND
from context import Context


def coverage(context: Context) -> None:
    context.python_run(
        "coverage",
        "erase",
        "run --omit=macrobond_data_api/common/enums/**,tests/** -m "
        + UNITTEST_COMMAND,
        "html",
        "report -m",
        "erase",
    )
    file_url = os.path.join(os.getcwd(), "htmlcov", "index.html").replace("\\", "/")
    print("file:///" + file_url)


def coverage_com(context: Context) -> None:
    context.python_run(
        "coverage",
        "erase",
        "run --include=macrobond_data_api/com/com_api.py,"
        + "macrobond-data-api/com/** -m "
        + UNITTEST_COMMAND,
        "html -d htmlcov_com",
        "report -m",
        "erase",
    )
    file_url = os.path.join(os.getcwd(), "htmlcov_com", "index.html").replace("\\", "/")
    print("file:///" + file_url)


def coverage_web(context: Context) -> None:
    context.python_run(
        "coverage",
        "erase",
        "run --include=macrobond_data_api/web/web_api.py,"
        + "macrobond_data_api/web/** -m "
        + UNITTEST_COMMAND,
        "html -d htmlcov_web",
        "report -m",
        "erase",
    )
    file_url = os.path.join(os.getcwd(), "htmlcov_web", "index.html").replace("\\", "/")
    print("file:///" + file_url)


def main():
    Context(coverage, coverage_com, coverage_web)


if __name__ == "__main__":
    main()
