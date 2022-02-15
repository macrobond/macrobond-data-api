
import sys
from context import Context


def coverage(context: Context) -> None:
    run = 'run --omit=macrobond_financial/common/enums/**,tests/** ' + \
        '-m unittest discover -v -s .\\tests -p **.py'
    context.install_and_run(
        'coverage',
        'erase',
        run,
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
