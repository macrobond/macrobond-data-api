from time import perf_counter

# import cProfile
from macrobond_data_api.web import WebClient, create_revision_history_request, SeriesWithVintages

#
#
# def test_get_fetch_all_vintageseries(*names: str) -> None:
#    def _callback(_: SeriesWithVintages):  # pylint: disable=unused-argument
#        ...
#
#    with WebClient() as api:
#        api.get_one_entity("usgdp")
#        start_timmer = perf_counter()
#        api.get_fetch_all_vintageseries(
#            _callback,
#            list(map(create_revision_history_request, names)),
#        )
#    time = perf_counter() - start_timmer
#    print(f"{str(len(names)):5} {f'{time:0.4f}':11}{time / len(names):0.5f}")
#
#
# def test_get_fetch_all_vintageseries_cProfile(*names: str) -> None:
#    def _callback(_: SeriesWithVintages):  # pylint: disable=unused-argument
#        ...
#
#    with WebClient() as api:
#        api.get_one_entity("usgdp")
#        start_timmer = perf_counter()
#        with cProfile.Profile() as pr:
#            api.get_fetch_all_vintageseries(
#                _callback,
#                list(map(create_revision_history_request, names)),
#            )
#            pr.print_stats(True)
#            print(f"{str(len(names)):5} {perf_counter() - start_timmer:0.4f}")
#
#
# if __name__ == "__main__":
#    # test_get_fetch_all_vintageseries_cProfile(*list(map(lambda _: "usgdp", range(1))))
#    for x in range(2, 40, 3):
#        test_get_fetch_all_vintageseries(*list(map(lambda _: "usgdp", range(x))))
#
#
# fetch_all_vintage_series
#
#
# with WebClient() as api:
#     start_timmer = perf_counter()
#     r = api.session.post("v1/series/fetchallvintageseries", json=[])
#     r.json()
#     print(f"[] {perf_counter() - start_timmer:0.4f} seconds")
#
# with WebClient() as api:
#     start_timmer = perf_counter()
#     r = api.session.post(
#         "v1/series/fetchallvintageseries", json=[create_revision_history_request("usgdp")]
#     )
#     r.json()
#     print(f"[usgdp] {perf_counter() - start_timmer:0.4f} seconds")
#
# with WebClient() as api:
#     start_timmer = perf_counter()
#     r = api.session.post(1
#         "v1/series/fetchallvintageseries",
#         json=[create_revision_history_request("usgdp"), create_revision_history_request("uscpi")],
#     )
#     print(r.text)
#     print(f"[usgdp, uscpi] {perf_counter() - start_timmer:0.4f} seconds")


def test():
    timmer_1 = perf_counter()
    with WebClient() as api:
        api.get_one_entity("usgdp")

        # print(f"with WebClient() as api: {perf_counter() - timmer_1:0.4f} seconds")
        # print("--- get_subscription_list")

        timmer_1 = perf_counter()
        api.get_subscription_list()
        print(f"api.get_subscription_list() {perf_counter() - timmer_1:0.4f} seconds")

        # print("--- get_subscription_list_iterative")

        def body(_):
            ...

        # print(f"body {perf_counter() - timmer_1:0.4f} seconds")

        def item(_):
            ...

        # print(f"item {perf_counter() - timmer_1:0.4f} seconds")

        timmer_1 = perf_counter()
        api.get_subscription_list_iterative(body, item)

        print(
            f"api.get_subscription_list_iterative(usgdp , uscpi) {perf_counter() - timmer_1:0.4f}"
        )


#
#     test_get_fetch_all_vintageseries("usgdp")
#
#     test_get_fetch_all_vintageseries("uscpi")
#
#     test_get_fetch_all_vintageseries("uscpi", "uscpi")
