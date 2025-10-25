import pytest
import pytest_asyncio

from app.core.cache.memory import InMemoryTranslationCache


@pytest_asyncio.fixture
async def cache():
    """Create a fresh in-memory cache for each test."""
    return InMemoryTranslationCache()


@pytest.mark.asyncio
async def test_cache_set_and_get(cache):
    """Test setting and getting values from cache."""
    await cache.set("key1", "value1")
    result = await cache.get("key1")
    assert result == "value1"


@pytest.mark.asyncio
async def test_cache_get_nonexistent(cache):
    """Test getting non-existent key returns None."""
    result = await cache.get("nonexistent")
    assert result is None


@pytest.mark.asyncio
async def test_cache_exists(cache):
    """Test exists method."""
    await cache.set("key1", "value1")
    assert await cache.exists("key1") is True
    assert await cache.exists("nonexistent") is False


@pytest.mark.asyncio
async def test_cache_clear(cache):
    """Test clearing cache."""
    await cache.set("key1", "value1")
    await cache.set("key2", "value2")
    assert cache.get_cache_size() == 2

    await cache.clear()
    assert cache.get_cache_size() == 0
    assert await cache.get("key1") is None


@pytest.mark.asyncio
async def test_cache_make_key(cache):
    """Test cache key generation."""
    key = cache._make_key("hello", "EN", "ES")
    # Should be a 64-character SHA256 hex digest
    assert isinstance(key, str)
    assert len(key) == 64

    key2 = cache._make_key("hello", "EN", "ES")
    assert key == key2
