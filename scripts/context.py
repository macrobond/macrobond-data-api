import os
import sys
import asyncio
import time
from typing import Any, Callable, List, NoReturn, Optional, cast, Sequence


def encode_if(str_: str, else_if: str) -> str:
    return str_ if sys.stdout.encoding == "utf-8" else else_if


class _ShellCommand:
    def __init__(self, command: str, ignore_exit_code: bool, exit_code: int, stdout: str, stderr: str) -> None:
        self.command = command
        self.ignore_exit_code = ignore_exit_code
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self) -> str:
        ret = f'"{self.command}"'

        if self.ignore_exit_code:
            ret += ", ignore_exit_code: True,"

        ret += " "
        if self.ignore_exit_code is False:
            ret += encode_if("✅", "(Ok)") if self.exit_code == 0 else encode_if("❌", "(Error)")
        else:
            ret += encode_if("❔", "(?)")

        ret += f" exit code: {self.exit_code}"

        return ret

    @property
    def is_error(self) -> bool:
        return not self.ignore_exit_code and self.exit_code != 0


class WorkItem:
    def __init__(self, in_sequence: bool, python_path: str) -> None:
        self.in_sequence = in_sequence
        self.python_path = python_path
        self.hade_error = False
        self.commands: List[_ShellCommand] = []
        self.out = ""

    def __bool__(self) -> bool:
        return self.hade_error

    def __lt__(self, other: Any) -> bool:
        return self.hade_error and not other.hade_error

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    @property
    def symbole(self) -> str:
        return encode_if("❌", "(Error)") if self.hade_error else encode_if("✅", "(Ok)")

    async def _run(self) -> None:
        await self.run()
        print(self.name + " " + self.symbole, end=" | ", flush=True)

    async def run(self) -> None: ...

    def print(self, object_: object) -> None:
        if self.in_sequence:
            print(object_)
        else:
            self.out += str(object_) + "\n"

    async def python_run(self, name: Optional[str], *args: str, ignore_exit_code: bool = False) -> None:
        prefix = f'"{self.python_path }" '

        for arg in args:
            command = f"-m {name} {arg}" if name else arg

            self.print("shell_command start :" + command)

            if self.in_sequence:
                exit_code = os.system(prefix + command)

                shell_command = _ShellCommand(command, ignore_exit_code, exit_code, "", "")
            else:
                proc = await asyncio.create_subprocess_shell(
                    prefix + command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await proc.communicate()
                exit_code = cast(int, proc.returncode)

                shell_command = _ShellCommand(
                    command, ignore_exit_code, cast(int, proc.returncode), stdout.decode(), stderr.decode()
                )
                self.print("stdout")
                self.print(shell_command.stdout)
                self.print("stderr")
                self.print(shell_command.stderr)

            self.print("shell_command end :" + command)
            self.print("exit_code " + str(exit_code))

            self.commands.append(shell_command)

            if shell_command.is_error:
                self.hade_error = True


async def _run_all(in_sequence: bool, work_items: Sequence) -> Any:
    if in_sequence:
        for work_item in work_items:
            print("Start " + work_item.name)
            await work_item.run()
            print("End " + work_item.name)
    else:
        print(f"Running the {len(work_items)} work items: ", end="", flush=True)
        await asyncio.gather(*[x._run() for x in work_items])
        print("")


def run(*work: Callable[[bool, str], WorkItem], in_sequence: bool = True) -> NoReturn:
    start_time = time.time()
    python_path = sys.executable
    work_items = [x(in_sequence, python_path) for x in work]

    if in_sequence:
        asyncio.run(_run_all(in_sequence, work_items))
    else:
        if os.name != "nt":
            raise ValueError("in_sequence == False is only supported on window.")
        loop = asyncio.ProactorEventLoop()  # type: ignore
        asyncio.set_event_loop(loop)  # type: ignore
        loop.run_until_complete(_run_all(in_sequence, work_items))  # type: ignore

    if not in_sequence:
        for work_item in work_items:
            print("Start " + work_item.name)
            print(work_item.out)
            print("End " + work_item.name)

    elapsed = time.time() - start_time
    print("elapsed: seconds " + str(elapsed))
    print("in_sequence: " + str(in_sequence))
    print("python_path: " + python_path)

    print("")

    print("--- WorkItems ---")
    for work_item in sorted(work_items):
        print(work_item.name + " " + work_item.symbole)
        if work_item.hade_error:
            print(work_item.out)

    print("")

    if any(work_items):
        print("Hade Errors " + encode_if("❌", "(Error)"))
        sys.exit(1)

    print("No Errors " + encode_if("✅", "(Ok)"))

    sys.exit()
