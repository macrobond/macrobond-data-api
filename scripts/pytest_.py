from context import WorkItem, run


class PyTest(WorkItem):
    async def run(self) -> None:
        await self.python_run("pytest", "-n auto -p no:faulthandler --durations=30")


if __name__ == "__main__":
    run(PyTest)
