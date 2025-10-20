from pydantic import BaseModel, Field


class LanguageResponse(BaseModel):
    """Language response model."""

    code: str
    name: str


class TranslationRequest(BaseModel):
    """Single translation request."""

    text: str = Field(..., description="Text to translate", min_length=1)
    source_language: str = Field(default="AUTO", description="Source language code")
    target_language: str = Field(default="EN", description="Target language code")


class TranslationResponse(BaseModel):
    """Single translation response."""

    original_text: str
    translated_text: str
    source_language: str
    target_language: str


class BatchTranslationRequest(BaseModel):
    """Batch translation request."""

    texts: list[str] = Field(..., description="List of texts to translate")
    source_language: str = Field(default="AUTO", description="Source language code")
    target_language: str = Field(default="EN", description="Target language code")


class BatchTranslationResponse(BaseModel):
    """Batch translation response."""

    translations: list[TranslationResponse]
