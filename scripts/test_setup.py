import os
import re
from typing import List
from context import WorkItem, run


class TestSetup(WorkItem):
    async def run(self) -> None:
        path = os.path.join(os.getcwd(), "setup.py")
        with open(path, "r", encoding="utf8") as f:
            content = f.read()

        match: List[str] = re.findall('"requests(?:\\>\\=|\\[socks]\\>\\=)[0-9]+\\.[0-9]+\\.[0-9]+"', content)
        print("match:\n", "\n".join(match), sep="")
        if len(match) != 3:
            self.hade_error = True
            print("len(match) != 3")
            return

        pattern = re.compile("[0-9]+\\.[0-9]+\\.[0-9]+")
        match_set = {re.findall(pattern, x)[0] for x in match}
        print("match_set:\n", "\n".join(match_set), sep="")
        if len(match_set) != 1:
            self.hade_error = True
            print("len(match_set) != 1")
            return


def main() -> None:
    run(TestSetup)


if __name__ == "__main__":
    main()
