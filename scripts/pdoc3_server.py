from context import WorkItem, run


class Pdoc3Server(WorkItem):
    async def run(self) -> None:
        await self.python_run("pdoc", " --http : --html --template-dir docs --force -o docs/build macrobond_data_api")


if __name__ == "__main__":
    run(Pdoc3Server)
