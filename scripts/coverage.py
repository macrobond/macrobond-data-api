import os
import sys
from context import run, WorkItem


async def _coverage(work_item: WorkItem, run_comand: str, dir_name: str) -> None:
    await work_item.python_run(
        "coverage",
        "erase",
        "run " + run_comand,
        "html -d " + dir_name,
        "report -m",
        "erase",
    )
    file_url = os.path.join(os.getcwd(), dir_name, "index.html").replace("\\", "/")
    work_item.print("file:///" + file_url)


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
            "htmlcov_com",
        )


class WebCoverage(WorkItem):
    async def run(self) -> None:
        await _coverage(
            self,
            "--include=macrobond_data_api/web/web_api.py,macrobond_data_api/web/** -m pytest -p no:faulthandler",
            "htmlcov_web",
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
            "htmlcov_comparison_com",
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
            "htmlcov_comparison_web",
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
