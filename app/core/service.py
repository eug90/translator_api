import logging

from app.core.cache.base import TranslationCache
from app.core.models import Language, TranslationResult
from app.core.providers.base import TranslationProvider

logger = logging.getLogger(__name__)


class TranslationService:
    """Service for managing translations with caching and provider flexibility."""

    def __init__(self, provider: TranslationProvider, cache: TranslationCache):
        """
        Initialize translation service.

        Args:
            provider: Translation provider instance
            cache: Translation cache instance
        """
        self.provider = provider
        self.cache = cache

    async def translate(
        self,
        text: str,
        source_language: str = "AUTO",
        target_language: str = "EN",
    ) -> TranslationResult:
        """
        Translate a single text.

        Args:
            text: Text to translate
            source_language: Source language code (default: AUTO)
            target_language: Target language code (default: EN)

        Returns:
            TranslationResult with original and translated text

        Raises:
            ValueError: If language is not supported
            Exception: If translation fails
        """
        # Check cache first
        cache_key = self.cache._make_key(text, source_language, target_language)
        cached_result = await self.cache.get(cache_key)

        if cached_result:
            print(f"Cache hit for key: {cache_key}")
            logger.info(f"Cache hit for key: {cache_key}")
            return TranslationResult(
                original_text=text,
                translated_text=cached_result,
                source_language=source_language,
                target_language=target_language,
            )
        logger.info(f"Cache miss for key: {cache_key}")
        # Translate using provider
        translated_text = await self.provider.translate(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )

        # Cache the result
        await self.cache.set(cache_key, translated_text)

        return TranslationResult(
            original_text=text,
            translated_text=translated_text,
            source_language=source_language,
            target_language=target_language,
        )

    async def translate_batch(
        self,
        texts: list[str],
        source_language: str = "AUTO",
        target_language: str = "EN",
    ) -> list[TranslationResult]:
        """
        Translate multiple texts.

        Args:
            texts: List of texts to translate
            source_language: Source language code (default: AUTO)
            target_language: Target language code (default: EN)

        Returns:
            List of TranslationResult objects

        Raises:
            ValueError: If language is not supported
            Exception: If translation fails
        """
        results = []

        # Check cache for each text
        texts_to_translate = []
        cached_texts = {}

        for text in texts:
            cache_key = self.cache._make_key(text, source_language, target_language)
            cached_result = await self.cache.get(cache_key)

            if cached_result:
                logger.info(f"Cache hit for key: {cache_key}")
                cached_texts[text] = cached_result
            else:
                texts_to_translate.append(text)

        # Translate uncached texts in batch
        if texts_to_translate:
            translated_texts = await self.provider.translate_batch(
                texts=texts_to_translate,
                source_language=source_language,
                target_language=target_language,
            )

            # Cache translated results
            for original, translated in zip(texts_to_translate, translated_texts):
                cache_key = self.cache._make_key(
                    original, source_language, target_language
                )
                await self.cache.set(cache_key, translated)

        # Build results list
        for text in texts:
            if text in cached_texts:
                translated_text = cached_texts[text]
            else:
                # Find in translated batch
                idx = texts_to_translate.index(text)
                translated_text = translated_texts[idx]

            results.append(
                TranslationResult(
                    original_text=text,
                    translated_text=translated_text,
                    source_language=source_language,
                    target_language=target_language,
                )
            )

        return results

    def get_supported_languages(self) -> list[Language]:
        """
        Get list of supported languages from the provider.

        Returns:
            List of Language objects
        """
        return self.provider.get_supported_languages()

    async def clear_cache(self) -> None:
        """Clear all cached translations."""
        await self.cache.clear()
