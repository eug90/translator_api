from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.api.dependencies import get_translation_service
from app.core.service import TranslationService

router = APIRouter(prefix="/translate", tags=["translation"])


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


@router.get("/languages", response_model=list[LanguageResponse])
async def get_supported_languages(
    service: TranslationService = Depends(get_translation_service),
):
    """Get list of supported languages."""
    languages = service.get_supported_languages()
    return [LanguageResponse(code=lang.code, name=lang.name) for lang in languages]


@router.post("/", response_model=TranslationResponse)
async def translate(
    request: TranslationRequest,
    service: TranslationService = Depends(get_translation_service),
):
    """
    Translate a single text.

    - **text**: Text to translate
    - **source_language**: Source language code (default: AUTO)
    - **target_language**: Target language code (default: EN)
    """
    try:
        result = await service.translate(
            text=request.text,
            source_language=request.source_language,
            target_language=request.target_language,
        )
        return TranslationResponse(
            original_text=result.original_text,
            translated_text=result.translated_text,
            source_language=result.source_language,
            target_language=result.target_language,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@router.post("/batch", response_model=BatchTranslationResponse)
async def translate_batch(
    request: BatchTranslationRequest,
    service: TranslationService = Depends(get_translation_service),
):
    """
    Translate multiple texts in batch.

    - **texts**: List of texts to translate
    - **source_language**: Source language code (default: AUTO)
    - **target_language**: Target language code (default: EN)
    """
    try:
        results = await service.translate_batch(
            texts=request.texts,
            source_language=request.source_language,
            target_language=request.target_language,
        )
        return BatchTranslationResponse(
            translations=[
                TranslationResponse(
                    original_text=result.original_text,
                    translated_text=result.translated_text,
                    source_language=result.source_language,
                    target_language=result.target_language,
                )
                for result in results
            ]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")
