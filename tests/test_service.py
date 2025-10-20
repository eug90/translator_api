from unittest.mock import AsyncMock

import pytest

from app.core.cache.memory import InMemoryTranslationCache
from app.core.models import Language
from app.core.service import TranslationService


class MockProvider:
    """Mock translation provider for testing."""

    def __init__(self):
        self.translate = AsyncMock(return_value="translated text")
        self.translate_batch = AsyncMock(return_value=["translated1", "translated2"])

    def get_supported_languages(self):
        return [
            Language("EN", "English"),
            Language("ES", "Spanish"),
        ]

    def is_language_supported(self, code: str):
        return code in ["EN", "ES", "AUTO"]


@pytest.fixture
def service():
    """Create a translation service with mock provider and real cache."""
    provider = MockProvider()
    cache = InMemoryTranslationCache()
    return TranslationService(provider=provider, cache=cache)


@pytest.mark.asyncio
async def test_translate_single_text(service):
    """Test translating a single text."""
    result = await service.translate("hello", "EN", "ES")

    assert result.original_text == "hello"
    assert result.translated_text == "translated text"
    assert result.source_language == "EN"
    assert result.target_language == "ES"


@pytest.mark.asyncio
async def test_translate_uses_cache(service):
    """Test that translation uses cache on second call."""
    # First call
    result1 = await service.translate("hello", "EN", "ES")
    assert service.provider.translate.call_count == 1

    # Second call should use cache
    result2 = await service.translate("hello", "EN", "ES")
    assert result1.translated_text == result2.translated_text
    assert service.provider.translate.call_count == 1  # Not called again


@pytest.mark.asyncio
async def test_translate_different_languages_no_cache(service):
    """Test that different language pairs don't use same cache."""
    await service.translate("hello", "EN", "ES")
    await service.translate("hello", "EN", "FR")

    # Should be called twice since it's different target language
    assert service.provider.translate.call_count == 2


@pytest.mark.asyncio
async def test_translate_batch(service):
    """Test batch translation."""
    results = await service.translate_batch(["hello", "world"], "EN", "ES")

    assert len(results) == 2
    assert results[0].original_text == "hello"
    assert results[1].original_text == "world"


@pytest.mark.asyncio
async def test_translate_batch_with_cache(service):
    """Test batch translation uses cache."""
    # First batch
    await service.translate_batch(["hello", "world"], "EN", "ES")
    assert service.provider.translate_batch.call_count == 1

    # Second batch with same texts should use cache
    await service.translate_batch(["hello", "world"], "EN", "ES")
    assert service.provider.translate_batch.call_count == 1  # Not called again


@pytest.mark.asyncio
async def test_translate_batch_partial_cache(service):
    """Test batch translation with partial cache hit."""
    # Cache one text
    await service.translate("hello", "EN", "ES")

    # Translate batch with one cached and one new
    results = await service.translate_batch(["hello", "world"], "EN", "ES")

    assert len(results) == 2
    # Only "world" should trigger a translate_batch call
    assert service.provider.translate_batch.call_count == 1


def test_get_supported_languages(service):
    """Test getting supported languages."""
    languages = service.get_supported_languages()

    assert len(languages) == 2
    assert languages[0].code == "EN"
    assert languages[1].code == "ES"


@pytest.mark.asyncio
async def test_clear_cache(service):
    """Test clearing cache."""
    await service.translate("hello", "EN", "ES")
    assert service.cache.get_cache_size() == 1

    await service.clear_cache()
    assert service.cache.get_cache_size() == 0
