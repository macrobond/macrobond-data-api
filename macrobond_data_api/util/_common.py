import io
import os
import sys
import pathlib
from typing import Any, Literal, Optional, cast


class SaveOutputToFile:
    fs: Optional[io.TextIOWrapper]

    def __init__(self, file_name: str):
        self.path = os.path.join(pathlib.Path.home(), file_name + ".txt")
        self.stdout = sys.stdout
        self.fs: Optional[io.TextIOWrapper] = None

    def write(self, data: str) -> None:
        if self.fs is not None:
            self.fs.write(data)
            self.fs.flush()
        self.stdout.write(data)

    def flush(self) -> None:
        if self.fs is not None:
            self.fs.flush()
        self.stdout.flush()

    def __enter__(self) -> "SaveOutputToFile":
        if _inquiry("Do you want to save the program output to a file? (" + self.path + ")"):
            self.fs = open(self.path, "w+", encoding="utf8")
            sys.stdout = cast(Any, self)

        return self

    def __exit__(self, exception_type: Any, exception_value: Any, traceback: Any) -> None:
        if self.fs is not None:
            self.fs.close()
            sys.stdout = self.stdout
            print("Output saved to file:", self.path)


_InquiryDefault = Literal["yes", "no", None]


def _inquiry(question: str, default: _InquiryDefault = "yes") -> bool:
    valid = {"yes": True, "y": True, "no": False, "n": False}
    if default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        default = None
        prompt = " [y/n] "

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        if choice in valid:
            return valid[choice]
        sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
