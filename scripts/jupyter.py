import json
import os
import sys
import pathlib
from typing import Any, Dict, List, Optional, Generator, Tuple
from context import WorkItem, run


def scrub_directory(directory_path: str) -> Generator[str, None, None]:
    for path in pathlib.Path(directory_path).rglob("*.ipynb"):
        hade_output: bool = False
        with open(path, encoding="UTF8") as file:
            json_obj: Optional[Dict[str, Any]] = json.loads(file.read())
        if json_obj is None:
            continue
        cells: Optional[List[Dict[str, Any]]] = json_obj.get("cells")
        if cells is None:
            continue
        for cell in cells:
            execution_count: Optional[List[dict]] = cell.get("execution_count")
            if execution_count and execution_count != 0:
                cell["execution_count"] = 0
                hade_output = True
            outputs: Optional[List[dict]] = cell.get("outputs")
            if not outputs or len(outputs) == 0:
                continue
            hade_output = True
            cell["outputs"] = []
        if hade_output:
            with open(path, "w", encoding="UTF8") as file:
                file.write(json.dumps(json_obj, indent=1) + "\n")
            yield str(path)[len(directory_path) :]


def verify_directory(directory_path: str) -> Generator[Tuple[str, str], None, None]:
    for path in pathlib.Path(directory_path).rglob("*.ipynb"):
        with open(path, encoding="UTF8") as file:
            json_obj: Optional[Dict[str, Any]] = json.loads(file.read())
        if json_obj is None:
            continue
        cells: Optional[List[Dict[str, Any]]] = json_obj.get("cells")
        if cells is None:
            continue
        for cell in cells:
            execution_count: Optional[List[dict]] = cell.get("execution_count")
            if execution_count and execution_count != 0:
                yield (str(path)[len(directory_path) :], "execution_count")
                continue
            outputs: Optional[List[dict]] = cell.get("outputs")
            if not outputs or len(outputs) == 0:
                continue
            yield (str(path)[len(directory_path) :], json.dumps(outputs, indent=2))


class JupyterVerify(WorkItem):
    async def run(self) -> None:
        directory = os.path.join(os.getcwd(), "examples")
        print("directory " + directory)
        for path, _ in verify_directory(directory):
            self.print('Error "' + path + '" has outputs')
            # self.>print(josn_outputs)
            self.hade_error = True

        if self.hade_error:
            print("run task jupyter scrub to fix")


class JupyterScrub(WorkItem):
    async def run(self) -> None:
        directory = os.path.join(os.getcwd(), "examples")
        print("directory " + directory)
        for path in scrub_directory(directory):
            self.print('"' + path + '" was scrub')


def main() -> None:
    command = sys.argv[1] if len(sys.argv) <= 2 else None

    if command == "--verify":
        run(JupyterVerify)

    if command == "--scrub":
        run(JupyterScrub)

    if command:
        print("bad args " + command)
    else:
        print("no args")

    sys.exit(1)


if __name__ == "__main__":
    main()
