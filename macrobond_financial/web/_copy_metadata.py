from typing import Any, Dict


def _copy_metadata(
    source: Dict[str, Any], destination: Dict[str, Any]
) -> Dict[str, Any]:
    for key in source.keys():
        destination["MetaData." + key] = source[key]
    return destination
