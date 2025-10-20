from app.core.cache.base import TranslationCache


class InMemoryTranslationCache(TranslationCache):
    """In-memory implementation of translation cache."""

    def __init__(self):
        """Initialize the in-memory cache."""
        self._cache: dict[str, str] = {}

    async def get(self, key: str) -> str | None:
        """
        Get a cached translation.

        Args:
            key: Cache key

        Returns:
            Cached translation or None if not found
        """
        return self._cache.get(key)

    async def set(self, key: str, value: str) -> None:
        """
        Set a cached translation.

        Args:
            key: Cache key
            value: Translation value
        """
        self._cache[key] = value

    async def exists(self, key: str) -> bool:
        """
        Check if a key exists in cache.

        Args:
            key: Cache key

        Returns:
            True if key exists, False otherwise
        """
        return key in self._cache

    async def clear(self) -> None:
        """Clear all cached translations."""
        self._cache.clear()

    def get_cache_size(self) -> int:
        """Get the current size of the cache."""
        return len(self._cache)
