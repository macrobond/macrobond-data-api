import os
import re
import sys
from typing import List
from context import WorkItem


class TestSetup(WorkItem):
    async def run(self) -> None:
        await self.python_run(None, os.path.join("scripts", "test_setup.py"))


def main() -> None:
    path = os.path.join(os.getcwd(), "setup.py")
    with open(path, "r", encoding="utf8") as f:
        content = f.read()

    match: List[str] = re.findall('"requests(?:\\>\\=|\\[socks]\\>\\=)[0-9]+\\.[0-9]+\\.[0-9]+"', content)
    print("match:\n", "\n".join(match), sep="")
    if len(match) != 3:
        print("len(match) != 3")
        sys.exit(1)

    pattern = re.compile("[0-9]+\\.[0-9]+\\.[0-9]+")
    match_set = {re.findall(pattern, x)[0] for x in match}
    print("match_set:\n", "\n".join(match_set), sep="")
    if len(match_set) != 1:
        print("len(match_set) != 1")
        sys.exit(1)


if __name__ == "__main__":
    main()
