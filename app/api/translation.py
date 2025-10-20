from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_translation_service
from app.api.schemas import (
    BatchTranslationRequest,
    BatchTranslationResponse,
    LanguageResponse,
    TranslationRequest,
    TranslationResponse,
)
from app.core.service import TranslationService

router = APIRouter(prefix="/translate", tags=["translation"])


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
