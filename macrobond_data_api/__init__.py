"""
Exposes a common API in Python for the Macrobond Web and Client Data APIs
"""


from ._macrobond_data_api import (
    metadata_list_values,
    metadata_get_attribute_information,
    metadata_get_value_information,
    get_all_vintage_series,
    get_nth_release,
    get_revision_info,
    get_vintage_series,
    get_observation_history,
    get_one_series,
    get_series,
    get_one_entity,
    get_entities,
    get_unified_series,
)
