import os
from unittest import UNITTEST_COMMAND
from context import Context


def coverage(context: Context) -> None:
    context.install_and_run(
        "coverage",
        "erase",
        "run --omit=macrobond_financial/common/enums/**,tests/** -m "
        + UNITTEST_COMMAND,
        "html",
        "report -m",
        "erase",
    )
    file_url = os.path.join(os.getcwd(), "htmlcov", "index.html").replace("\\", "/")
    print("file:///" + file_url)


def coverage_com(context: Context) -> None:
    context.install_and_run(
        "coverage",
        "erase",
        "run --omit=macrobond_financial/common/**,macrobond_financial/com/**,"
        + "macrobond_financial/web/web_typs/**,tests/** -m "
        + UNITTEST_COMMAND,
        "html -d htmlcov_com",
        "report -m",
        "erase",
    )
    file_url = os.path.join(os.getcwd(), "htmlcov_com", "index.html").replace("\\", "/")
    print("file:///" + file_url)


def coverage_web(context: Context) -> None:
    context.install_and_run(
        "coverage",
        "erase",
        "run --omit=macrobond_financial/common/**,macrobond_financial/web/**,"
        + "macrobond_financial/com/com_typs/**,tests/** -m "
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
