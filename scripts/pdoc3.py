import os
import shutil
from context import WorkItem, run


class Pdoc3(WorkItem):
    async def run(self) -> None:
        await self.python_run("pdoc", " --html --template-dir docs --force -o docs/build macrobond_data_api")

        if os.path.isdir("docs/build/macrobond_data_api/assets"):
            shutil.rmtree("docs/build/macrobond_data_api/assets")
        shutil.copytree("docs/assets", "docs/build/macrobond_data_api/assets")

        file_url = os.path.join(os.getcwd(), "docs", "build", "macrobond_data_api", "index.html").replace("\\", "/")

        self.print("file:///" + file_url)


if __name__ == "__main__":
    run(Pdoc3)
