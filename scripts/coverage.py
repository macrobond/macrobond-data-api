import os
from context import run, WorkItem


class Coverage(WorkItem):
    async def run(self) -> None:
        await self.python_run(
            "coverage",
            "erase",
            "run --omit=macrobond_data_api/common/enums/**,tests/** -m pytest",
            "html",
            "report -m",
            "erase",
        )
        file_url = os.path.join(os.getcwd(), "htmlcov", "index.html").replace("\\", "/")
        self.print("file:///" + file_url)


class ComCoverage(WorkItem):
    async def run(self) -> None:
        await self.python_run(
            "coverage",
            "erase",
            "run --include=macrobond_data_api/com/com_api.py," + "macrobond-data-api/com/** -m pytest",
            "html -d htmlcov_com",
            "report -m",
            "erase",
        )
        file_url = os.path.join(os.getcwd(), "htmlcov_com", "index.html").replace("\\", "/")
        self.print("file:///" + file_url)


class WebCoverage(WorkItem):
    async def run(self) -> None:
        await self.python_run(
            "coverage",
            "erase",
            "run --include=macrobond_data_api/web/web_api.py," + "macrobond_data_api/web/** -m pytest",
            "html -d htmlcov_web",
            "report -m",
            "erase",
        )
        file_url = os.path.join(os.getcwd(), "htmlcov_web", "index.html").replace("\\", "/")
        self.print("file:///" + file_url)


if __name__ == "__main__":
    run(Coverage, ComCoverage, WebCoverage, in_sequence=False)
