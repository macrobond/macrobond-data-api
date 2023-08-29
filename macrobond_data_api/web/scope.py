from enum import Enum


class Scope(Enum):
    READ_MB = "macrobond_web_api.read_mb"
    SEARCH_MB = "macrobond_web_api.search_mb"
    READ_STRUCTURE = "macrobond_web_api.read_structure"
    WRITE_IH = "macrobond_web_api.write_ih"
