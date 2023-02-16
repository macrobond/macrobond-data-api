from context import WorkItem, run


class Black(WorkItem):
    async def run(self) -> None:
        await self.python_run("black", "--extend-exclude macrobond_data_api_python_env .")


if __name__ == "__main__":
    run(Black)
