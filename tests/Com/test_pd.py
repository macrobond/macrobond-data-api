import pandas as pd
from macrobond_data_api.com import ComClient


def test_pd_datetime() -> None:
    pd_timestamp = pd.to_datetime("2022-07-01").tz_localize("utc")
    datetime = pd_timestamp.to_pydatetime()
    with ComClient() as mda:
        mda.get_observation_history("uslama4760", pd_timestamp)
        mda.get_observation_history("uslama4760", datetime)
