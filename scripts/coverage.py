import os
import sys
from context import run, WorkItem


async def _coverage(work_item: WorkItem, run_comand: str, dir_name: str) -> None:
    await work_item.python_run(
        "coverage",
        "erase",
        "run " + run_comand,
        "html -d " + os.path.join("htmlcov", dir_name),
        "report -m",
        "erase",
    )

    def file_url(url: str) -> str:
        return "file:///" + url.replace("\\", "/")

    def file_url_to_htmlcov(dir_name: str) -> str:
        return file_url(os.path.join(os.getcwd(), "htmlcov", dir_name, "index.html"))

    with open(os.path.join(os.getcwd(), "htmlcov", "index.html"), "w", encoding="utf8") as f:
        f.write(
            f'<a href="{file_url_to_htmlcov("com")}">com</a></br>'
            + f'<a href="{file_url_to_htmlcov("web")}">web</a>'
            + f'</br> <a href="{file_url_to_htmlcov("htmlcov")}">htmlcov</a></br>'
        )

    work_item.print(file_url(os.path.join(os.getcwd(), "htmlcov", "index.html")))


class Coverage(WorkItem):
    async def run(self) -> None:
        await _coverage(
            self, "--omit=macrobond_data_api/common/enums/**,tests/** -m pytest -p no:faulthandler", "htmlcov"
        )


class ComCoverage(WorkItem):
    async def run(self) -> None:
        await _coverage(
            self,
            "--include=macrobond_data_api/com/com_api.py,macrobond_data_api/com/** -m pytest -p no:faulthandler",
            "com",
        )


class WebCoverage(WorkItem):
    async def run(self) -> None:
        await _coverage(
            self,
            "--include=macrobond_data_api/web/web_api.py,macrobond_data_api/web/** -m pytest -p no:faulthandler",
            "web",
        )


class ComComparisonCoverage(WorkItem):
    async def run(self) -> None:
        files = ",".join(
            [
                "macrobond_data_api/com/_com_api_metadata.py",
                "macrobond_data_api/com/_com_api_revision.py",
                "macrobond_data_api/com/_com_api_search.py",
                "macrobond_data_api/com/_com_api_series.py",
                "macrobond_data_api/com/_com_only_api.py",
            ]
        )

        await _coverage(
            self,
            f"--include={files} -m pytest ./tests/comparison_tests/ -p no:faulthandler",
            "comparison_com",
        )


class WebComparisonCoverage(WorkItem):
    async def run(self) -> None:
        files = ",".join(
            [
                "macrobond_data_api/web/_web_api_metadata.py",
                "macrobond_data_api/web/_web_api_revision.py",
                "macrobond_data_api/web/_web_api_search.py",
                "macrobond_data_api/web/_web_api_series.py",
                "macrobond_data_api/web/_web_only_api.py",
            ]
        )

        await _coverage(
            self,
            f"--include={files} -m pytest ./tests/comparison_tests/ -p no:faulthandler",
            "comparison_web",
        )


def main() -> None:
    command = sys.argv[1] if len(sys.argv) <= 2 else None

    if command == "--all":
        run(Coverage, ComCoverage, WebCoverage)

    if command == "--web":
        run(WebCoverage)

    if command == "--com":
        run(ComCoverage)

    if command == "--comparison":
        run(ComComparisonCoverage, WebComparisonCoverage)

    if command:
        print("bad args " + command)
    else:
        print("no args")

    sys.exit(1)


if __name__ == "__main__":
    main()
