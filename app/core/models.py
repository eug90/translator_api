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
