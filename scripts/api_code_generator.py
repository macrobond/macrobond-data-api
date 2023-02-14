import ast
import os
import sys
from typing import Optional, Type, Union

from context import Context

from code_generator import CodeGenerator


class _ApiCodeGenerator(CodeGenerator):
    def __init__(self, type_: Type) -> None:
        super().__init__(type_)
        self.prefix = "return _get_api()."

        get_api_inport = ast.ImportFrom()
        get_api_inport.module = "._get_api"
        alias = ast.alias()
        alias.name = "_get_api"
        get_api_inport.names = [alias]
        self.analyzer.includs.append(get_api_inport)

    def filter_includs(self, node: Union[ast.Import, ast.ImportFrom]) -> Optional[Union[ast.Import, ast.ImportFrom]]:
        module = node.module  # type: ignore

        if not module:
            raise ValueError("module is None")

        if module == "abc":
            return None

        if module == "types":
            node.module = "macrobond_data_api.common.types"  # type: ignore
            return node

        if module == "enums":
            node.module = "macrobond_data_api.common.enums"  # type: ignore
            return node

        return node


def _write_to_file(path: str, code: str) -> None:
    with open(path, "w+", encoding="UTF8") as file:
        file.write(code)


def _verify_file(path: str, code: str) -> int:
    with open(path, "r", encoding="UTF8") as file:
        if file.read() != code:
            print("Failed verification " + path)
            return 1
    return 0


def main() -> None:
    paths = {
        "_generated": os.path.join("macrobond_data_api", "_generated.py"),
        "__init__": os.path.join("macrobond_data_api", "__init__.py"),
    }

    sys.path.append(os.getcwd())
    from macrobond_data_api.common.api import Api  # pylint: disable=import-outside-toplevel import-error

    sys.path.pop()

    generator = _ApiCodeGenerator(Api)

    code = {
        "_generated": generator.run(),
        "__init__": generator.format(
            "\n".join(
                [
                    "#",
                    "# This is generated code, do not edit",
                    "#",
                    "",
                    "'''",
                    "Exposes a common API in Python for the Macrobond Web and Client Data APIs",
                    "'''",
                    "",
                    ("from ._macrobond_data_api import " + (",".join(x.name for x in generator.analyzer.functions))),
                ],
            )
        ),
    }

    if len(sys.argv) <= 2 and sys.argv[1] == "--generate":
        _write_to_file(paths["_generated"], code["_generated"])
        _write_to_file(paths["__init__"], code["__init__"])
        print("Code generated")
        sys.exit(0)

    if len(sys.argv) <= 2 and sys.argv[1] == "--verify":
        exit_code = 0
        exit_code += _verify_file(paths["_generated"], code["_generated"])
        exit_code += _verify_file(paths["__init__"], code["__init__"])

        if exit_code == 0:
            print("successful verification")

        sys.exit(exit_code)

    print("no args, use --verify or --generate")
    sys.exit(1)


def verify(context: Context) -> None:
    context.shell_command(context.python_path + " " + os.path.join("scripts", "api_code_generator.py") + " --verify")


def generate(context: Context) -> None:
    context.shell_command(context.python_path + " " + os.path.join("scripts", "api_code_generator.py") + " --generate")


if __name__ == "__main__":
    main()
