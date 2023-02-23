from context import WorkItem, run


class Pycodestyle(WorkItem):
    async def run(self) -> None:
        await self.python_run("pycodestyle", "--count . --exclude=.env")


if __name__ == "__main__":
    run(Pycodestyle)
