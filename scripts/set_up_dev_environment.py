from context import WorkItem, run


class SetUpDevEnvironment(WorkItem):
    async def run(self) -> None:
        await self.python_run("pip", "install --upgrade pip")
        await self.python_run("pip", "uninstall -y macrobond-data-api", ignore_exit_code=True)
        await self.python_run("pip", "install -e .[dev,extra]")


if __name__ == "__main__":
    run(SetUpDevEnvironment)
