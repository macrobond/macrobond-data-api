import pandas as pd  # type: ignore
from macrobond_data_api.com import ComClient


def test_pd_datetime() -> None:
    pd_datetime = pd.to_datetime("2022-07-01").tz_localize("utc")
    with ComClient() as mda:
        mda.get_observation_history("uslama4760", pd_datetime)
