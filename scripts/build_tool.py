from context import WorkItem, run


class BuildTool(WorkItem):
    async def run(self) -> None:
        await self.python_run(None, "-m build")


if __name__ == "__main__":
    run(BuildTool)
