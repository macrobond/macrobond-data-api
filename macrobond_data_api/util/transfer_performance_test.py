#!/usr/bin/env python3

from urllib import request

from time import perf_counter
from typing import List, Optional, Sequence
from datetime import timedelta

import requests


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


def _get_url(size_kB: int) -> str:
    return f"https://api.macrobondfinancial.com/utilities/teststream?length={size_kB}"


class _Result:
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
        if body_time.total_seconds() != 0:
            self.kBs = size_kB / body_time.total_seconds()
        else:
            self.kBs = 0

    @staticmethod
    def run_integrity_test(size_kB: int, i: int) -> "_Result":
        try:
            start_time = perf_counter()
            response = requests.get(_get_url(size_kB), timeout=60 * 2)
            content_length_kb = int(len(response.content) / 1024)
            end_time = perf_counter()

            total_time = timedelta(seconds=end_time - start_time)

            if size_kB != content_length_kb:
                return _Result(
                    size_kB,
                    Exception(
                        f"Content length does not match, expected {size_kB} but got {content_length_kb}. n = {i}"
                    ),
                )

            try:
                _Result._test_data(size_kB, response.content)
            except ValueError as ex:
                return _Result(size_kB, ex)

            return _Result(size_kB, None, content_length_kb, response.elapsed, total_time, response.status_code)
        except requests.exceptions.RequestException as ex:
            return _Result(size_kB, ex)

    @staticmethod
    def _test_data(size_kB: int, content: bytes) -> None:
        segments = content.split(b">")

        if len(segments) != size_kB + 1:
            raise ValueError("Wrong number of segments")

        segments.pop(len(segments) - 1)

        for i, segment in enumerate(segments):
            header = bytes(f"<{str(i).zfill(5)}:", "us-ascii")
            if not segment.startswith(header):
                raise ValueError("Wrong segment header")

            if len(segment) != 1023:
                raise ValueError("Wrong segment length")

            if segment[7:] != _Result._test_body:
                raise ValueError("Wrong body length")


class _ResultList:
    def __init__(self, size_kB: int):
        self.size_kB = size_kB
        if size_kB < 1:
            self.name = f"{size_kB * 1024:.0f} B"
        if size_kB < 1024:
            self.name = f"{size_kB:.0f} kB"
        else:
            self.name = f"{size_kB / 1024:.0f} MB"
        self.reslults: List[_Result] = []

    def run_integrity_tests(self, indicator: bool, times: int) -> None:
        print(f"Testing {self.name} ", end="", flush=True)
        for i in range(0, times):
            result = _Result.run_integrity_test(self.size_kB, i)
            if result.error is not None:
                pass
                # print(f" Error: {str(result.error)} ", end="", flush=True)
            elif indicator:
                print(".", end="", flush=True)

            self.reslults.append(result)
        print(" done")

    def display_results(self) -> None:
        resultes = [x for x in self.reslults if x.error is None]

        if len(resultes) == 0:
            print(f"Too few results for {self.name}")
            return

        total_seconds = [x.total_time.total_seconds() for x in resultes]
        # headers_times = [x.headers_time.total_seconds() for x in resultes]
        # kBs = [x.kBs for x in resultes]

        print(f"Result for {self.name}")

        # print("\tTotal time")
        print(f"Average time {_average(total_seconds):.2f} s")
        print(f"Max time {max(total_seconds):.2f} s")
        print(f"Min time {min(total_seconds):.2f} s")

        # print("\tHeader time")
        # print(f"\t\tAverage time {_average(headers_times):.2f} s")
        # print(f"\t\tMax time {max(headers_times):.2f} s")
        # print(f"\t\tMin time {min(headers_times):.2f} s")

        # print("\tSpeed")
        # print(f"\t\tAverage {_format_speed_kB_sec(_average(kBs))}")
        # print(f"\t\tMax {_format_speed_kB_sec(max(kBs))}")
        # print(f"\t\tMin {_format_speed_kB_sec(min(kBs))}")

        print("")


def _speed_test() -> None:
    results = []
    size_kB = 10 * 1024

    for _ in range(0, 10):
        with request.urlopen(request.Request(_get_url(size_kB))) as response:
            start_time = perf_counter()
            _ = response.read()
            end_time = perf_counter()
            total_time = timedelta(seconds=end_time - start_time)

            results.append(size_kB / total_time.total_seconds())

    print(f"Speed {_format_speed_kB_sec(_average(results))}\n")


def _integrity_test(sizes_kB: Sequence[int], times: int, indicator: bool) -> None:
    result_lists: List[_ResultList] = [_ResultList(x) for x in sizes_kB]

    print(f"Testing sizes [{', '.join([x.name for x in result_lists])}]\n")

    for result_list in result_lists:
        result_list.run_integrity_tests(indicator, times)

    all_resultes: List[_Result] = sum([x.reslults for x in result_lists], [])

    print()

    errors = [x for x in all_resultes if x.error is not None]
    if len(errors) == 0:
        print("All done, No errors")
    else:
        print(f"All done, {len(errors)} errors !")
        for error in errors:
            print(f"\t{error.size_kB} kB Error: {error.error}")
        print("")

    # kBs = [x.kBs for x in all_resultes if x.error is None]
    # if len(kBs) == 0:
    #     print("Too few results")
    #     return

    print("")

    for result_list in result_lists:
        result_list.display_results()


def transfer_performance_test(sizes_kB: Optional[Sequence[int]] = None, times: int = 4, indicator: bool = True) -> None:
    # Run speed and integrity test.
    # The integrity test verifies that data is transferred correctly.
    print("- transfer performance test beginning -\n")

    print("- Running speed test -")
    _speed_test()

    print("- Running integrity test -")
    _integrity_test(sizes_kB if sizes_kB else [10, 100, 1024, 10 * 1024], times, indicator)

    print("- transfer performance test end -")


if __name__ == "__main__":
    transfer_performance_test()
