import os
import io
import sys
import ast
import inspect

from typing import List, Union, Type, Callable, Optional

from context import WorkItem

from black import format_str, Mode


class FunctionInfo:
    def __init__(self, name: str, function: Callable[[], None]) -> None:
        self.name = name
        self.function = function
        doc = inspect.getdoc(function)
        self.doc = doc if doc else ""
        self.signature = inspect.signature(function)

        source = inspect.getsource(self.function)
        source = source.replace("\n", "")
        i = source.index("(")
        source = source[i:]
        i = source.index(")")
        i = i + source[i:].index(":")
        source = source[: i + 1]
        source = source.replace("self,", "")
        self.definition = source

    def get_indentd_doc(self, indent: str) -> str:
        return "".join("\n" if x == "" else indent + x + "\n" for x in self.doc.split("\n"))


class Analyzer(ast.NodeVisitor):
    def __init__(self, type_: Type) -> None:
        source_path = inspect.getfile(type_)

        self.includs: List[Union[ast.Import, ast.ImportFrom]] = []

        with open(source_path, "r", encoding="UTF8") as source:
            tree = ast.parse(source.read())

        self.visit(tree)

        self.functions: List[FunctionInfo] = [
            FunctionInfo(name, function)
            for name, function in inspect.getmembers(type_, inspect.isfunction)
            if not name.startswith("_")
        ]

    # pylint: disable=invalid-name

    def visit_Import(self, node: ast.Import) -> None:
        self.includs.append(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.includs.append(node)
        self.generic_visit(node)

    # pylint: enable=invalid-name


class CodeGenerator:
    def __init__(
        self, includs: List[Union[ast.Import, ast.ImportFrom]] = None, functions: List[FunctionInfo] = None
    ) -> None:
        self.includs = includs if includs else []
        self.functions = functions if functions else []
        # self.analyzer = Analyzer(type_)
        # self.analyzer.includs = [x for x in (self.filter_includs(x) for x in self.analyzer.includs) if x]
        self._out = io.StringIO()
        self.indent = "".ljust(4, " ")
        self.prefix = ""
        self.comment_heading = "This is generated code, do not edit"
        self.source = ""

    def __str__(self) -> str:
        return self.source

    def format(self, code: str) -> str:
        return format_str(code, mode=Mode(line_length=120))

    def run(self) -> None:
        write = self._out.write

        write("#\n# " + self.comment_heading + "\n#\n\n")

        self.write_imcluds()

        write("\n")

        self.write_functions()

        self._out.seek(0)
        self.source = self.format(self._out.read())

        self._out.close()

    def write_functions(self) -> None:
        write = self._out.write

        def write_functions_parameters(function: FunctionInfo) -> None:
            first = True
            for par in list(function.signature.parameters.values())[1:]:
                if not first:
                    write(", ")
                first = False

                if par.kind == par.POSITIONAL_OR_KEYWORD:
                    write(par.name)
                elif par.kind == par.POSITIONAL_ONLY:
                    raise NotImplementedError(par.kind)
                elif par.kind == par.VAR_KEYWORD:
                    raise NotImplementedError(par.kind)
                elif par.kind == par.VAR_POSITIONAL:
                    write("*" + par.name)
                elif par.kind == par.KEYWORD_ONLY:
                    write(par.name + " = " + par.name)
                else:
                    raise NotImplementedError(par.kind)

        for function in self.functions:
            write(f"def {function.name} {function.definition}\n")
            write(f'{self.indent}"""\n')
            write(function.get_indentd_doc(self.indent))
            write(f'{self.indent}"""\n')

            write(f"{self.indent}{self.prefix}{function.name}(")
            write_functions_parameters(function)
            write(")\n")

    def write_imcluds(self) -> None:
        write = self._out.write

        def import_(node: ast.Import) -> None:
            module = node.module  # type: ignore
            if not module:
                raise ValueError("module is None")
            write(f"import {module}\n")

        def from_(node: ast.ImportFrom) -> None:
            module = node.module  # type: ignore
            if not module:
                raise ValueError("module is None")

            names = ", ".join(x.name for x in node.names)
            write(f"from {module} import {names}\n")

        for node in self.includs:
            if isinstance(node, ast.Import):
                import_(node)
            else:
                from_(node)


class ApiCodeGenerator(CodeGenerator):
    def __init__(self) -> None:
        super().__init__()
        self.prefix = "return _get_api()."

        sys.path.append(os.getcwd())
        from macrobond_data_api.common.api import Api  # pylint: disable=import-outside-toplevel import-error

        sys.path.pop()

        analyzer = Analyzer(Api)

        self.includs += [x for x in map(self.filter_includs, analyzer.includs) if x]
        self.functions = analyzer.functions

        get_api_inport = ast.ImportFrom()
        get_api_inport.module = "._get_api"
        alias = ast.alias()
        alias.name = "_get_api"
        get_api_inport.names = [alias]
        self.includs.append(get_api_inport)

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

    generator = ApiCodeGenerator()
    generator.run()

    code = {
        "_generated": str(generator),
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
                    ("from ._generated import " + (",".join(x.name for x in generator.functions))),
                ],
            )
        ),
    }

    command = sys.argv[1] if len(sys.argv) <= 2 else None

    if command == "--generate":
        _write_to_file(paths["_generated"], code["_generated"])
        _write_to_file(paths["__init__"], code["__init__"])
        print("Code generated")
        sys.exit(0)

    if command == "--verify":
        exit_code = 0
        exit_code += _verify_file(paths["_generated"], code["_generated"])
        exit_code += _verify_file(paths["__init__"], code["__init__"])

        if exit_code == 0:
            print("successful verification")

        sys.exit(exit_code)

    print("no args, use --verify or --generate")
    sys.exit(1)


class Verify(WorkItem):
    async def run(self) -> None:
        await self.python_run(None, os.path.join("scripts", "code_generation.py") + " --verify")


class Generate(WorkItem):
    async def run(self) -> None:
        await self.python_run(None, os.path.join("scripts", "code_generation.py") + " --generate")


if __name__ == "__main__":
    main()
