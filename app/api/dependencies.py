from app.core.cache.memory import InMemoryTranslationCache
from app.core.config import settings
from app.core.providers.deepl import DeepLProvider
from app.core.service import TranslationService

# Initialize cache and provider
_cache = InMemoryTranslationCache()
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
