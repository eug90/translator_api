from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Language:
    """Represents a supported language."""

    code: str
    name: str


@dataclass
class TranslationResult:
    """Result of a translation operation."""

    original_text: str
    translated_text: str
    source_language: str
    target_language: str


class TranslationProvider(ABC):
    """Abstract base class for translation providers."""

    @abstractmethod
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
            Exception: If translation fails
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def get_supported_languages(self) -> list[Language]:
        """
        Get list of supported languages.

        Returns:
            List of Language objects
        """
        pass

    @abstractmethod
    def is_language_supported(self, language_code: str) -> bool:
        """
        Check if a language is supported.

        Args:
            language_code: Language code to check

        Returns:
            True if supported, False otherwise
        """
        pass
