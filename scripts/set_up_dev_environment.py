import shutil
import os
from context import WorkItem, run


class SetUpDevEnvironment(WorkItem):
    async def run(self) -> None:
        git_hooks = os.path.join(os.getcwd(), ".git", "hooks")
        scripts_hooks = os.path.join(os.getcwd(), "scripts", "git_hooks")

        shutil.copyfile(os.path.join(scripts_hooks, "pre-commit"), os.path.join(git_hooks, "pre-commit"))
        shutil.copyfile(os.path.join(scripts_hooks, "pre-push"), os.path.join(git_hooks, "pre-push"))

        await self.python_run("pip", "install --upgrade pip")
        await self.python_run("pip", "uninstall -y macrobond-data-api", ignore_exit_code=True)
        await self.python_run("pip", "install -e .[dev,extra]")


if __name__ == "__main__":
    run(SetUpDevEnvironment)
