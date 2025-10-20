from abc import ABC, abstractmethod


class TranslationCache(ABC):
    """Abstract base class for translation caching."""

    @abstractmethod
    async def get(self, key: str) -> str | None:
        """
        Get a cached translation.

        Args:
            key: Cache key

        Returns:
            Cached translation or None if not found
        """
        pass

    @abstractmethod
    async def set(self, key: str, value: str) -> None:
        """
        Set a cached translation.

        Args:
            key: Cache key
            value: Translation value
        """
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """
        Check if a key exists in cache.

        Args:
            key: Cache key

        Returns:
            True if key exists, False otherwise
        """
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all cached translations."""
        pass

    def _make_key(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:
        """
        Generate a cache key from translation parameters.

        Args:
            text: Text to translate
            source_language: Source language code
            target_language: Target language code

        Returns:
            Cache key
        """
        return f"{source_language}:{target_language}:{text}"
