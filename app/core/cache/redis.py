import redis.asyncio as redis

from app.core.cache.base import TranslationCache


class RedisTranslationCache(TranslationCache):
    """Redis-based implementation of translation cache."""

    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        """
        Initialize the Redis cache.

        Args:
            redis_url: Redis connection URL
        """
        self.redis_url = redis_url
        self._client: redis.Redis | None = None

    async def _get_client(self) -> redis.Redis:
        """
        Get or create Redis client connection.

        Returns:
            Redis async client
        """
        if self._client is None:
            self._client = await redis.from_url(self.redis_url, decode_responses=True)
        return self._client

    async def get(self, key: str) -> str | None:
        """
        Get a cached translation.

        Args:
            key: Cache key

        Returns:
            Cached translation or None if not found
        """
        client = await self._get_client()
        return await client.get(key)

    async def set(self, key: str, value: str, ttl: int = 86400) -> None:
        """
        Set a cached translation.

        Args:
            key: Cache key
            value: Translation value
            ttl: Time to live in seconds (default: 24 hours)
        """
        client = await self._get_client()
        await client.set(key, value, ex=ttl)

    async def exists(self, key: str) -> bool:
        """
        Check if a key exists in cache.

        Args:
            key: Cache key

        Returns:
            True if key exists, False otherwise
        """
        client = await self._get_client()
        return await client.exists(key) > 0

    async def clear(self) -> None:
        """Clear all cached translations."""
        client = await self._get_client()
        await client.flushdb()

    async def close(self) -> None:
        """Close Redis connection."""
        if self._client is not None:
            await self._client.close()
            self._client = None

    def get_cache_size(self) -> int:
        """
        Get the current size of the cache.

        Note: This is a placeholder. Redis doesn't have a direct sync method for this.
        Use async_get_cache_size() instead.

        Returns:
            0 (use async_get_cache_size for actual count)
        """
        return 0

    async def async_get_cache_size(self) -> int:
        """
        Get the current size of the cache asynchronously.

        Returns:
            Number of keys in Redis
        """
        client = await self._get_client()
        return await client.dbsize()
