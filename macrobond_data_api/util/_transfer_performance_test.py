#!/usr/bin/env python3

from time import perf_counter
from typing import List, Optional, Sequence
from datetime import timedelta

import requests

#
# 1 s for hedder (för att få ner hedder)
# 2 megabits is ok (sepeed)
#


def _format_speed_kB_sec(kB: float) -> str:
    return _format_kB(kB) + "/s"


def _format_kB(kB: float) -> str:
    if kB < 1:
        return f"{kB * 1024:.2f} B"
    if kB < 1024:
        return f"{kB:.2f} kB"
    return f"{kB / 1024:.2f} MB"


def _average(sequence: Sequence[float]) -> float:
    return sum(sequence) / len(sequence)


class _Resultet:
    _test_body = bytearray(("0123456789" * 101) + "012345", "us-ascii")

    def __init__(
        self,
        size_kB: int,
        error: Optional[Exception],
        content_length_kB: int = -1,
        headers_time: timedelta = timedelta.max,
        total_time: timedelta = timedelta.max,
        status_code: int = -1,
    ):
        self.size_kB = size_kB
        self.error = error
        self.content_length_kB = content_length_kB
        self.headers_time = headers_time
        self.total_time = total_time
        self.status_code = status_code
        body_time = total_time - headers_time
        self.body_time = body_time
        self.kBs = size_kB / body_time.total_seconds()


class _ResultetList:
    def __init__(self, size_kB: int):
        self.size_kB = size_kB
        if size_kB < 1:
            self.name = f"{size_kB * 1024:.0f} B"
        if size_kB < 1024:
            self.name = f"{size_kB:.0f} kB"
        else:
            self.name = f"{size_kB / 1024:.0f} MB"
        self.reslults: List[_Resultet] = []

    def run_tests(self, indicator: bool, times: int) -> None:
        print(f"Testing {self.name} ", end="", flush=True)
        for i in range(0, times):
            result = self._run_test(i)
            if result.error is not None:
                print(f" Error: {str(result.error)} ", end="", flush=True)
            elif indicator:
                print(".", end="", flush=True)

            self.reslults.append(result)
        print(" done")

    def _run_test(self, i: int) -> _Resultet:
        url = f"https://api.macrobondfinancial.com/utilities/teststream?length={self.size_kB}"
        try:
            start_time = perf_counter()
            response = requests.get(url, timeout=60 * 2)
            content_length_kb = int(len(response.content) / 1024)
            end_time = perf_counter()

            total_time = timedelta(seconds=end_time - start_time)

            if self.size_kB != content_length_kb:
                return _Resultet(
                    self.size_kB,
                    Exception(
                        f"Content length does not match, expected {self.size_kB} but got {content_length_kb}. n = {i}"
                    ),
                )

            try:
                self.test_data(response.content)
            except ValueError as ex:
                return _Resultet(self.size_kB, ex)

            return _Resultet(self.size_kB, None, content_length_kb, response.elapsed, total_time, response.status_code)
        except requests.exceptions.RequestException as ex:
            return _Resultet(self.size_kB, ex)

    def test_data(self, content: bytes) -> None:
        segments = content.split(b">")

        if len(segments) != self.size_kB + 1:
            raise ValueError("Wrong number of segments")

        segments.pop(len(segments) - 1)

        for i, segment in enumerate(segments):
            header = bytes(f"<{str(i).zfill(5)}:", "us-ascii")
            if not segment.startswith(header):
                raise ValueError("Wrong segment header")

            if len(segment) != 1023:
                raise ValueError("Wrong segment length")

            if segment[7:] != _Resultet._test_body:
                raise ValueError("Wrong body length")

    def display_resultets(self) -> None:
        resultes = [x for x in self.reslults if x.error is None]

        if len(resultes) == 0:
            print(f"Too few results for {self.name}")
            return

        total_seconds = [x.total_time.total_seconds() for x in resultes]
        headers_times = [x.headers_time.total_seconds() for x in resultes]
        kBs = [x.kBs for x in resultes]

        print(f"Resulte for {self.name}")

        print("\tTotal time")
        print(f"\t\tAverage time {_average(total_seconds):.2f} s")
        print(f"\t\tMax time {max(total_seconds):.2f} s")
        print(f"\t\tMin time {min(total_seconds):.2f} s")

        print("\tHeader time")
        print(f"\t\tAverage time {_average(headers_times):.2f} s")
        print(f"\t\tMax time {max(headers_times):.2f} s")
        print(f"\t\tMin time {min(headers_times):.2f} s")

        print("\tSpeed")
        print(f"\t\tAverage {_format_speed_kB_sec(_average(kBs))}")
        print(f"\t\tMax {_format_speed_kB_sec(max(kBs))}")
        print(f"\t\tMin {_format_speed_kB_sec(min(kBs))}")

        print("")


def transfer_performance_test(sizes_kB: Optional[Sequence[int]] = None, times: int = 4, indicator: bool = True) -> None:
    if sizes_kB is None:
        sizes_kB = [10, 100, 1000, 1 * 1024, 10 * 1024, 20 * 1024, 30 * 1024, 40 * 1024, 50 * 1024]

    resultet_lists: List[_ResultetList] = [_ResultetList(x) for x in sizes_kB]

    print(f"Running transfer performance test for {', '.join([x.name for x in resultet_lists])}\n")

    for resultet_list in resultet_lists:
        resultet_list.run_tests(indicator, times)

    print("Resultes\n")

    all_resultes: List[_Resultet] = sum([x.reslults for x in resultet_lists], [])

    errors = [x for x in all_resultes if x.error is not None]
    if len(errors) == 0:
        print("No errors\n")
    else:
        print(f"{len(errors)} errors !")
        for error in errors:
            print(f"\tError: {error.error}")
        print("")

    kBs = [x.kBs for x in all_resultes if x.error is None]

    print("Speed")
    print(f"Average {_format_speed_kB_sec(_average(kBs))}")
    print(f"Max {_format_speed_kB_sec(max(kBs))}")
    print(f"Min {_format_speed_kB_sec(min(kBs))}")

    print("")

    for resultet_list in resultet_lists:
        resultet_list.display_resultets()


if __name__ == "__main__":
    # transfer_performance_test([2], 1)
    # transfer_performance_test([50_000], 1)
    transfer_performance_test()
    # transfer_performance_test([20_000], 100)
