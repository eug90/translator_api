from app.core.cache.base import TranslationCache
from app.core.cache.memory import InMemoryTranslationCache
from app.core.cache.redis import RedisTranslationCache
from app.core.config import settings
from app.core.providers.deepl import DeepLProvider
from app.core.service import TranslationService


def _create_cache() -> TranslationCache:
    """Create cache instance based on configuration."""
    if settings.cache_type.lower() == "redis":
        return RedisTranslationCache(redis_url=settings.redis_url)
    return InMemoryTranslationCache()


# Initialize cache and provider
_cache = _create_cache()
_provider = DeepLProvider(
    api_url=settings.deepl_api_url, api_key=settings.deepl_api_key
)
_service = TranslationService(provider=_provider, cache=_cache)


async def get_translation_service() -> TranslationService:
    """
    Dependency for getting the translation service instance.

    Returns:
        TranslationService instance
    """
    return _service
