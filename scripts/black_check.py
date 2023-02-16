from context import WorkItem, run


class BlackCheck(WorkItem):
    async def run(self) -> None:
        await self.python_run("black", "--extend-exclude macrobond_data_api_python_env --check --diff .")


if __name__ == "__main__":
    run(BlackCheck)
