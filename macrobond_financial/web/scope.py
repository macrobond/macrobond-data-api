# -*- coding: utf-8 -*-

from enum import Enum


class Scope(Enum):
    READ_MB = "macrobond_web_api.read_mb"
    SEARCH_MB = "macrobond_web_api.search_mb"
    READ_STRUCTURE = "macrobond_web_api.read_structure"
