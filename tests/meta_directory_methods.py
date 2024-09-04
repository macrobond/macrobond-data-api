import pytest
from macrobond_data_api.common import Api


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_get_attribute_information(api: Api) -> None:
    with pytest.raises(Exception):
        api.metadata_get_attribute_information("Description____")


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_list_values(api: Api) -> None:
    with pytest.raises(Exception):
        api.metadata_list_values("__RateType")

    with pytest.raises(Exception):
        api.metadata_list_values("Description")


@pytest.mark.parametrize("api", ["web", "com"], indirect=True)
def test_get_value_information(api: Api) -> None:
    with pytest.raises(ValueError, match="Unknown attribute: bad val"):
        api.metadata_get_value_information(("bad val", "mole"))

    with pytest.raises(ValueError, match="Unknown attribute value: RateType,bad val"):
        api.metadata_get_value_information(("RateType", "bad val"))

    with pytest.raises(ValueError, match="Unknown attribute value: RateType,bad val"):
        api.metadata_get_value_information(("RateType", "mole"), ("RateType", "bad val"))
