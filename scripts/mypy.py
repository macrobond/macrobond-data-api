from context import WorkItem, run

# https://mypy.readthedocs.io/en/stable/command_line.html


# TODO: @mb-jp use --strict for mypy


class Mypy(WorkItem):
    async def run(self) -> None:
        await self.python_run("mypy", ". --show-error-codes --exclude .env --python-version 3.7")


if __name__ == "__main__":
    run(Mypy)
