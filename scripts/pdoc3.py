# -*- coding: utf-8 -*-

import os
from context import Context


def pdoc3(context: Context) -> None:
    context.python_run(
        "pdoc",
        " --html --template-dir ./scripts/docs-templates "
        + "--force -o ./docs ./macrobond_data_api/",
    )

    file_url = os.path.join(os.getcwd(), "docs", "macrobond_data_api", "index.html").replace(
        "\\", "/"
    )

    print("file:///" + file_url)


if __name__ == "__main__":
    Context(pdoc3)
