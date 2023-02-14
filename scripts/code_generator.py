import io
import sys
import ast
import inspect
from typing import List, Type, Tuple, Callable, Union, Optional


class _FunctionInfo:
    def __init__(self, info: Tuple[str, Callable[[], None]]) -> None:
        self.name = info[0]
        self.function = info[1]
        doc = inspect.getdoc(self.function)
        self.doc = doc if doc else ""
        self.signature = inspect.signature(self.function)

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
        return "".join("\n" if x == "" else indent + x + "\n" for x in self.doc.split("\n")) + "\n"


class _Analyzer(ast.NodeVisitor):
    def __init__(self, type_: Type) -> None:
        source_path = inspect.getfile(type_)

        self.includs: List[Union[ast.Import, ast.ImportFrom]] = []

        with open(source_path, "r", encoding="UTF8") as source:
            tree = ast.parse(source.read())

        self.visit(tree)

        self.functions: List[_FunctionInfo] = [
            _FunctionInfo(x) for x in inspect.getmembers(type_, inspect.isfunction) if x[0] != "__init__"
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
    def __init__(self, type_: Type) -> None:
        self.analyzer = _Analyzer(type_)
        self.analyzer.includs = [x for x in (self.filter_includs(x) for x in self.analyzer.includs) if x]
        self._out = io.StringIO()
        self.indent = "".ljust(4, " ")
        self.prefix = ""
        self.comment_heading = "This is generated code, do not edit"
        self.source = ""

    def filter_includs(self, node: Union[ast.Import, ast.ImportFrom]) -> Optional[Union[ast.Import, ast.ImportFrom]]:
        return node

    def format(self, code: str) -> str:
        path_temp = sys.path[0]
        sys.path.remove(path_temp)

        # pylint: disable=import-outside-toplevel
        # pylint: disable=import-error
        # pylint: disable=no-name-in-module
        from black import format_str, Mode  # type: ignore

        # pylint: enable=import-outside-toplevel
        # pylint: enable=import-error
        # pylint: enable=no-name-in-module
        sys.path.insert(0, path_temp)

        return format_str(code, mode=Mode(line_length=120))

    def run(self) -> str:
        write = self._out.write

        write("#\n# " + self.comment_heading + "\n#\n\n")

        self.write_imcluds()

        write("\n")

        self.write_functions()

        self._out.seek(0)
        self.source = self.format(self._out.read())

        self._out.close()

        return self.source

    def write_functions(self) -> None:
        write = self._out.write

        def write_functions_parameters(function: _FunctionInfo) -> None:
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

        for function in self.analyzer.functions:
            write(f"def {function.name} {function.definition}\n")
            write(f'{self.indent}"""\n')
            write(function.get_indentd_doc(self.indent) + "\n")
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

        for node in self.analyzer.includs:
            if isinstance(node, ast.Import):
                import_(node)
            else:
                from_(node)
