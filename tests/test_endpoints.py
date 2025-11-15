from unittest.mock import AsyncMock, create_autospec, patch

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_translation_service
from app.api.main import app
from app.core.cache.memory import InMemoryTranslationCache
from app.core.providers.base import TranslationProvider
from app.core.service import TranslationService


def test_get_supported_languages(client):
    """Test getting supported languages endpoint."""
    response = client.get("/api/v1/translate/languages")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 0


@pytest.fixture
def service():
    """Create a translation service with mock provider and real cache."""
    provider = create_autospec(TranslationProvider, spec_set=True)
    cache = InMemoryTranslationCache()
    return TranslationService(provider=provider, cache=cache)


@pytest.fixture
def client(service):
    """Create a test client for the FastAPI app."""
    client = TestClient(app)
    app.dependency_overrides[get_translation_service] = lambda: service
    return client


def test_translate_single_text(client, service):
    """Test single text translation endpoint."""
    service.provider.translate.return_value = "Здравствуйте, как поживаете?"

    response = client.post(
        "/api/v1/translate/",
        json={
            "text": "Hello, how are you?",
            "source_language": "EN",
            "target_language": "RU",
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["original_text"] == "Hello, how are you?"
    assert data["translated_text"] == "Здравствуйте, как поживаете?"

def test_translate_batch_text(client, service):
    """Test batch text translation endpoint."""
    service.provider.translate_batch.return_value = [
        "Здравствуйте",
        "Как дела?",
    ]

    response = client.post(
        "/api/v1/translate/batch",
        json={
            "texts": ["Hello", "How are you?"],
            "source_language": "EN",
            "target_language": "RU",
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert len(data["translations"]) == 2
    assert data["translations"][0]["original_text"] == "Hello"
    assert data["translations"][0]["translated_text"] == "Здравствуйте"
    assert data["translations"][1]["original_text"] == "How are you?"
    assert data["translations"][1]["translated_text"] == "Как дела?"
    
# def test_translate_batch(client):
#     """Test batch translation endpoint."""
#     with patch("app.api.dependencies.get_translation_service") as mock_service_dep:
#         mock_service = AsyncMock()

#         mock_result1 = type(
#             "obj",
#             (object,),
#             {
#                 "original_text": "hello",
#                 "translated_text": "hola",
#                 "source_language": "EN",
#                 "target_language": "ES",
#             },
#         )()

#         mock_result2 = type(
#             "obj",
#             (object,),
#             {
#                 "original_text": "world",
#                 "translated_text": "mundo",
#                 "source_language": "EN",
#                 "target_language": "ES",
#             },
#         )()

#         mock_service.translate_batch = AsyncMock(
#             return_value=[mock_result1, mock_result2]
#         )
#         mock_service_dep.return_value = mock_service

#         response = client.post(
#             "/api/v1/translate/batch",
#             json={
#                 "texts": ["hello", "world"],
#                 "source_language": "EN",
#                 "target_language": "ES",
#             },
#         )

#         assert response.status_code == 200
#         data = response.json()
#         assert "translations" in data
#         assert len(data["translations"]) == 2


def test_translate_unsupported_language_error(client):
    """Test translation with unsupported language returns error."""
    with patch("app.api.dependencies.get_translation_service") as mock_service_dep:
        mock_service = AsyncMock()
        mock_service.translate = AsyncMock(
            side_effect=ValueError("Target language 'XX' is not supported")
        )
        mock_service_dep.return_value = mock_service

        response = client.post(
            "/api/v1/translate/",
            json={
                "text": "hello",
                "source_language": "EN",
                "target_language": "XX",
            },
        )

        assert response.status_code == 400
