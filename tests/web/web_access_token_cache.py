from unittest.mock import Mock

import pytest

from macrobond_data_api.web._access_token_cache import _AccessTokenCache, _CacheItem

CACHE_KEY = "test_key"


@pytest.mark.no_account
class TestAccessTokenCache:

    def test_1(self) -> None:
        sut = _AccessTokenCache(CACHE_KEY)

        mock = Mock()
        mock.remove_old_time.side_effect = [10, 10, 10000]
        sut.remove_old_time = mock.remove_old_time

        _AccessTokenCache._cache.clear()
        _AccessTokenCache._cache[CACHE_KEY] = _CacheItem("", None, 10)

        assert sut._remove_old() == 0
        assert len(_AccessTokenCache._cache) == 1
        assert sut._get()

        assert sut._remove_old() == 1
        assert len(_AccessTokenCache._cache) == 0
        assert sut._get()

    def test_2(self) -> None:
        sut = _AccessTokenCache(CACHE_KEY)

        mock = Mock()
        mock.remove_old_time.side_effect = [10, 10, 10000, 10000, 20000]
        sut.remove_old_time = mock.remove_old_time

        _AccessTokenCache._cache.clear()
        _AccessTokenCache._cache[CACHE_KEY] = _CacheItem("", 10000, 10)

        assert sut._remove_old() == 0
        assert len(_AccessTokenCache._cache) == 1
        assert sut._get()

        assert sut._remove_old() == 0
        assert len(_AccessTokenCache._cache) == 1
        assert sut._get()

        assert sut._remove_old() == 1
        assert len(_AccessTokenCache._cache) == 0
        assert sut._get()
