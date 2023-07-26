import json
import os
import pathlib
import subprocess
import sys
from typing import Dict, List, Optional, TypedDict

import pytest


class IpynbCustom(TypedDict, total=False):
    metadata: Optional[dict]


class IpynbOutputs(TypedDict, total=False):
    data: Dict[str, List[str]]
    execution_count: int
    metadata: Optional[dict]
    output_type: str


class IpynbCell(TypedDict, total=False):
    cell_type: str
    outputs: Optional[IpynbOutputs]
    execution_count: Optional[int]
    metadata: Optional[dict]


class IpynbDoc(TypedDict, total=False):
    cells: List[IpynbCell]
    custom: Optional[dict]


def _test_jupyter_notebook(file_path: str) -> None:
    python_path = sys.executable
    with open(file_path, encoding="UTF8") as file:
        original_content = file.read()
        original_notebook: Optional[IpynbDoc] = json.loads(original_content)

    assert original_notebook

    try:
        result = subprocess.run(
            [python_path, "-m", "jupyter", "nbconvert", "--to", "notebook", "--inplace", "--execute", file_path],
            stdout=subprocess.PIPE,
            check=True,
        )

        assert result.returncode == 0, "stdout:\n" + result.stdout.decode()

        with open(file_path, encoding="UTF8") as file:
            new_content = file.read()
            new_notebook: Optional[IpynbDoc] = json.loads(new_content)
            assert new_notebook

        # new_notebook["custom"] = {}

        for cell in new_notebook["cells"]:
            if cell["cell_type"] != "code":
                continue
            cell["metadata"] = {}
            cell["execution_count"] = 1

        assert len(original_notebook) == len(new_notebook)

        for original_cell, new_cell in zip(original_notebook["cells"], new_notebook["cells"]):
            assert original_cell == new_cell

        assert original_notebook == new_notebook
    finally:
        with open(file_path, mode="w", encoding="UTF8") as file:
            file.write(original_content)


@pytest.mark.skip
@pytest.mark.parametrize("file", ["Metadata", "Revision", "Search", "Series"])
def test_file(file: str) -> None:
    target = os.path.join(pathlib.Path(__file__).parent.resolve(), "Jupyter", file + ".ipynb")
    _test_jupyter_notebook(target)


# jupyter nbconvert --to notebook --inplace --execute '.\examples\1.1 - Macrobond web API - Metadata Navigation.ipynb'
