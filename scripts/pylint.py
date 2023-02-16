from context import WorkItem, run


class Pylint(WorkItem):
    async def run(self) -> None:
        await self.python_run("pylint", "macrobond_data_api -f colorized -r y")


if __name__ == "__main__":
    run(Pylint)
