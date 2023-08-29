from datetime import datetime, timezone

from pandas.testing import assert_frame_equal

import pytest
from macrobond_data_api.common import Api
from macrobond_data_api.common.types import RevisionHistoryRequest
from macrobond_data_api.web import WebApi
from macrobond_data_api.com import ComApi


@pytest.mark.usefixtures("assert_no_warnings")
@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_com_and_web(api: Api) -> None:
    # get_revision_info
    result1 = api.get_revision_info("usgdp")[0]
    str(result1.to_pd_data_frame())
    result1.to_dict()

    # Get_vintage_series
    last_revision = api.get_revision_info("gbgdp")[0].time_stamp_of_last_revision

    if not last_revision:
        raise ValueError("last_revision is None")

    result2 = api.get_vintage_series(last_revision, ["gbgdp"])[0]
    str(result2.values_to_pd_data_frame())
    str(result2.metadata_to_pd_series())
    result2.to_dict()

    # Get_nth_release
    result3 = api.get_nth_release(4, ["gbgdp"])[0]
    str(result3.values_to_pd_data_frame())
    str(result3.metadata_to_pd_series())
    result3.to_dict()

    # Get_all_vintage_series
    result4 = api.get_all_vintage_series("usgdp")[0]
    str(result4.values_to_pd_data_frame())
    str(result4.metadata_to_pd_series())
    result4.to_dict()

    # Get_observation_history
    result5 = api.get_observation_history("usgdp", datetime(2022, 3, 27))[0]
    str(result5.to_pd_data_frame())
    result5.to_dict()
    result5.to_pd_series()


def test_common(web: WebApi, com: ComApi) -> None:
    assert_frame_equal(
        web.get_all_vintage_series("usgdp")[0].values_to_pd_data_frame(),
        com.get_all_vintage_series("usgdp")[0].values_to_pd_data_frame(),
    )

    assert_frame_equal(
        web.get_all_vintage_series("ustrad4488")[0].values_to_pd_data_frame(),
        com.get_all_vintage_series("ustrad4488")[0].values_to_pd_data_frame(),
    )

    assert_frame_equal(
        web.get_all_vintage_series("ct_au_e_ao_c_22_v")[0].values_to_pd_data_frame(),
        com.get_all_vintage_series("ct_au_e_ao_c_22_v")[0].values_to_pd_data_frame(),
    )

    # get_many_series_with_revisions

    for _ in com.get_many_series_with_revisions([]):
        ...

    for _ in web.get_many_series_with_revisions([]):
        ...

    _ = next(
        web.get_many_series_with_revisions([RevisionHistoryRequest("usgdp", datetime(2000, 2, 3, tzinfo=timezone.utc))])
    )
    _ = next(
        com.get_many_series_with_revisions([RevisionHistoryRequest("usgdp", datetime(2000, 2, 3, tzinfo=timezone.utc))])
    )
