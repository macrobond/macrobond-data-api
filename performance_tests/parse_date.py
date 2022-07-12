from datetime import datetime
from time import perf_counter

from dateutil import parser  # type: ignore


def _parse_date(date_text: str) -> datetime:
    return datetime(int(date_text[0:4]), int(date_text[5:7]), int(date_text[8:10]))


if __name__ == "__main__":
    TEXT = "1959-01-01T00:00:00"
    N = 10_00000

    print(_parse_date(TEXT))
    print(parser.parse(TEXT))

    print(_parse_date(TEXT).timetz)
    print(parser.parse(TEXT).timetz)

    start_timmer = perf_counter()
    for x in range(N):
        _parse_date(TEXT)
    print(f"new {str(N):5} {perf_counter() - start_timmer:0.4f}")

    start_timmer = perf_counter()
    for x in range(N):
        parser.parse(TEXT)
    print(f"old {str(N):5} {perf_counter() - start_timmer:0.4f}")
