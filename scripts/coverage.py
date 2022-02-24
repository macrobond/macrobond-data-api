
import sys
import os
from unittest import UNITTEST_COMMAND
from context import Context


def coverage(context: Context) -> None:
    context.install_and_run(
        'coverage',
        'erase',
        'run --omit=macrobond_financial/common/enums/**,tests/** -m ' + UNITTEST_COMMAND,
        'html',
        'report -m',
        'erase'
    )
    file_url = os.path.join(os.getcwd(), 'htmlcov', 'index.html').replace('\\', '/')
    print('file:///' + file_url)


def main():
    context = Context()
    coverage(context)
    if context.hade_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
