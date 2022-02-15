# -*- coding: utf-8 -*-

from context import Context


def pdoc3(context: Context) -> None:
    context.install_and_run(
        'pdoc',
        '--html --template-dir ./scripts/docs-templates --force -o ./docs ./macrobond_financial/'
    )


if __name__ == "__main__":
    Context(pdoc3)
