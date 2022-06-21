# -*- coding: utf-8 -*-

import os
from context import Context


def pdoc3server(context: Context) -> None:
    context.python_run(
        "pdoc",
        " --http : --html --template-dir ./scripts/docs-templates "
        + "--force -o ./docs ./macrobond_financial/",
        pip_name="pdoc3",
    )

    file_url = os.path.join(
        os.getcwd(), "docs", "macrobond_financial", "index.html"
    ).replace("\\", "/")

    print("file:///" + file_url)


if __name__ == "__main__":
    Context(pdoc3server)
