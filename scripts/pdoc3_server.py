# -*- coding: utf-8 -*-

import os
from context import Context


def pdoc3server(context: Context) -> None:
    context.python_run(
        "pdoc",
        " --http : --html --template-dir docs --force -o docs/build macrobond_data_api",
    )

    file_url = os.path.join(
        os.getcwd(), "docs", "build", "macrobond_data_api", "index.html"
    ).replace("\\", "/")

    print("file:///" + file_url)


if __name__ == "__main__":
    Context(pdoc3server)
