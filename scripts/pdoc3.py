# -*- coding: utf-8 -*-

import os
from context import Context, PYTHON_36


def pdoc3(context: Context, version_of_python: str = PYTHON_36) -> None:
    python_path = context.get_python_path(version_of_python)
    context.python_run(
        python_path,
        "pdoc",
        " --html --template-dir ./scripts/docs-templates "
        + "--force -o ./docs ./macrobond_financial/",
    )

    file_url = os.path.join(
        os.getcwd(), "docs", "macrobond_financial", "index.html"
    ).replace("\\", "/")

    print("file:///" + file_url)


if __name__ == "__main__":
    Context(pdoc3)
