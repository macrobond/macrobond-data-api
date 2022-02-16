
import sys
from context import Context
from unittest_310 import UNITTEST_COMMAND


def coverage(context: Context) -> None:
    context.install_and_run(
        'coverage',
        'erase',
        'run --omit=macrobond_financial/common/enums/**,tests/** -m ' + UNITTEST_COMMAND,
        'html',
        'report -m',
        'erase'
    )


def main():
    context = Context()
    coverage(context)
    if context.hade_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
