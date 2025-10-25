import pytest

from app.core.cache.redis import RedisTranslationCache


@pytest.fixture
async def redis_cache():
    """Create a fresh Redis cache for each test."""
    cache = RedisTranslationCache(redis_url="redis://localhost:6379/1")
    # Clear the test database before each test
    await cache.clear()
    yield cache
    # Cleanup after test
    await cache.close()


@pytest.mark.asyncio
async def test_redis_cache_set_and_get(redis_cache):
    """Test setting and getting values from Redis cache."""
    await redis_cache.set("key1", "value1")
    result = await redis_cache.get("key1")
    assert result == "value1"


@pytest.mark.asyncio
async def test_redis_cache_get_nonexistent(redis_cache):
    """Test getting non-existent key returns None."""
    result = await redis_cache.get("nonexistent")
    assert result is None


@pytest.mark.asyncio
async def test_redis_cache_exists(redis_cache):
    """Test exists method."""
    await redis_cache.set("key1", "value1")
    assert await redis_cache.exists("key1") is True
    assert await redis_cache.exists("nonexistent") is False


@pytest.mark.asyncio
async def test_redis_cache_clear(redis_cache):
    """Test clearing cache."""
    await redis_cache.set("key1", "value1")
    await redis_cache.set("key2", "value2")
    size = await redis_cache.async_get_cache_size()
    assert size == 2

    await redis_cache.clear()
    size = await redis_cache.async_get_cache_size()
    assert size == 0
    assert await redis_cache.get("key1") is None


@pytest.mark.asyncio
async def test_redis_cache_make_key(redis_cache):
    """Test cache key generation."""
    key = redis_cache._make_key("hello", "EN", "ES")
    assert isinstance(key, str)
    assert len(key) == 64  # SHA256 hex digest is 64 characters


@pytest.mark.asyncio
async def test_redis_cache_ttl(redis_cache):
    """Test that values expire based on TTL."""
    import asyncio

    await redis_cache.set("key1", "value1", ttl=1)
    assert await redis_cache.get("key1") == "value1"

    await asyncio.sleep(1.5)
    result = await redis_cache.get("key1")
    assert result is None


@pytest.mark.asyncio
async def test_redis_cache_size(redis_cache):
    """Test async_get_cache_size method."""
    await redis_cache.clear()
    size = await redis_cache.async_get_cache_size()
    assert size == 0

    await redis_cache.set("key1", "value1")
    size = await redis_cache.async_get_cache_size()
    assert size == 1

    await redis_cache.set("key2", "value2")
    size = await redis_cache.async_get_cache_size()
    assert size == 2
