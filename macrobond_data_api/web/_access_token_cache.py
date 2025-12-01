import time
from typing import Dict, Optional


class _CacheItem:
    def __init__(self, access_token: Optional[str], expires_at: Optional[int], created: float) -> None:
        self.access_token = access_token
        self.expires_at = expires_at
        self.created = created


class _AccessTokenCache:
    _cache: Dict[str, _CacheItem] = {}

    def __init__(self, key: Optional[str]) -> None:
        self._key = key
        self._no_key_cache_item = _CacheItem(None, None, 0)
        self.remove_old_time = time.time

    def _get(self) -> _CacheItem:
        self._remove_old()

        if self._key is None:
            return self._no_key_cache_item

        item = self._cache.get(self._key)
        if item is None:
            item = self._cache[self._key] = _CacheItem(None, None, time.time())

        return item

    def _remove_old(self) -> int:
        if len(self._cache) == 0:
            return 0

        now = self.remove_old_time()
        to_remove = []
        for key, item in self._cache.items():
            time_to_test = item.created
            if item.expires_at:
                time_to_test = item.expires_at
            if now - time_to_test > 7200:
                to_remove.append(key)

        for key in to_remove:
            del self._cache[key]

        return len(to_remove)
