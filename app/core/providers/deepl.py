import asyncio
import logging

from app.core.models import Language
from app.core.providers.base import TranslationProvider
from app.core.translator import call_remote_api

logger = logging.getLogger(__name__)


class DeepLProvider(TranslationProvider):
    """DeepL translation provider with retry mechanism."""

    # Supported languages (selected 3 as per requirement)
    SUPPORTED_LANGUAGES = [
        Language("EN", "English"),
        Language("ES", "Spanish"),
        Language("RU", "Russian"),
    ]

    def __init__(
        self,
        api_url: str,
        api_key: str,
        max_retries: int = 3,
        initial_delay: float = 0.5,
        exponential_base: float = 2.0,
        max_delay: float = 30.0,
    ):
        """
        Initialize DeepL provider.

        Args:
            api_url: DeepL API URL
            api_key: DeepL API key
            max_retries: Maximum number of retries for failed requests (default: 3)
            initial_delay: Initial delay in seconds (default: 0.5)
            exponential_base: Base for exponential backoff (default: 2.0)
            max_delay: Maximum delay cap in seconds (default: 30.0)
        """
        self.api_url = api_url
        self.api_key = api_key
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.exponential_base = exponential_base
        self.max_delay = max_delay

    async def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:
        """
        Translate text from source to target language.

        Args:
            text: Text to translate
            source_language: Source language code
            target_language: Target language code

        Returns:
            Translated text

        Raises:
            ValueError: If language is not supported
            Exception: If translation fails after retries
        """
        if not self.is_language_supported(target_language):
            raise ValueError(f"Target language '{target_language}' is not supported")

        if source_language != "AUTO" and not self.is_language_supported(
            source_language
        ):
            raise ValueError(f"Source language '{source_language}' is not supported")

        return await self._translate_with_retry(text, source_language, target_language)

    async def translate_batch(
        self,
        texts: list[str],
        source_language: str,
        target_language: str,
    ) -> list[str]:
        """
        Translate multiple texts from source to target language.

        Args:
            texts: List of texts to translate
            source_language: Source language code
            target_language: Target language code

        Returns:
            List of translated texts

        Raises:
            ValueError: If language is not supported
            Exception: If translation fails
        """
        if not self.is_language_supported(target_language):
            raise ValueError(f"Target language '{target_language}' is not supported")

        if source_language != "AUTO" and not self.is_language_supported(
            source_language
        ):
            raise ValueError(f"Source language '{source_language}' is not supported")

        # Translate all texts concurrently
        tasks = [
            self._translate_with_retry(text, source_language, target_language)
            for text in texts
        ]
        return await asyncio.gather(*tasks)

    def get_supported_languages(self) -> list[Language]:
        """
        Get list of supported languages.

        Returns:
            List of Language objects
        """
        return self.SUPPORTED_LANGUAGES

    def is_language_supported(self, language_code: str) -> bool:
        """
        Check if a language is supported.

        Args:
            language_code: Language code to check

        Returns:
            True if supported, False otherwise
        """
        if language_code == "AUTO":
            return True
        return any(
            lang.code == language_code.upper() for lang in self.SUPPORTED_LANGUAGES
        )

    def _calculate_backoff_delay(self, attempt: int) -> float:
        """
        Calculate exponential backoff delay with jitter and cap.

        Args:
            attempt: Retry attempt number (0-indexed)

        Returns:
            Delay in seconds (capped at max_delay)
        """
        delay = self.initial_delay * (self.exponential_base**attempt)
        # Cap the delay at max_delay
        return min(delay, self.max_delay)

    async def _translate_with_retry(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:
        """
        Translate with retry mechanism.

        Args:
            text: Text to translate
            source_language: Source language code
            target_language: Target language code

        Returns:
            Translated text

        Raises:
            Exception: If translation fails after all retries
        """
        last_error = None

        for attempt in range(self.max_retries):
            try:
                result = await call_remote_api(
                    url=self.api_url,
                    method="POST",
                    headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"},
                    json_data={
                        "text": [text],
                        "source_lang": source_language.upper(),
                        "target_lang": target_language.upper(),
                    },
                )

                if "translations" in result and result["translations"]:
                    return result["translations"][0].get("text", "")

                raise ValueError("Invalid response format from DeepL API")

            except Exception as e:
                last_error = e
                logger.warning(
                    f"Translation attempt {attempt + 1}/{self.max_retries} failed: {str(e)}"
                )

                if attempt < self.max_retries - 1:
                    delay = self._calculate_backoff_delay(attempt)
                    logger.debug(
                        f"Retrying in {delay:.2f}s (exponential backoff, attempt {attempt + 1})"
                    )
                    await asyncio.sleep(delay)

        raise Exception(
            f"Translation failed after {self.max_retries} retries"
        ) from last_error
