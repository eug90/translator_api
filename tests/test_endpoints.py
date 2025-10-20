from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.api.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_get_supported_languages(client):
    """Test getting supported languages endpoint."""
    response = client.get("/api/v1/translate/languages")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 0


def test_translate_single_text(client):
    """Test single text translation endpoint."""
    with patch("app.api.dependencies.get_translation_service") as mock_service_dep:
        mock_service = AsyncMock()
        mock_translation_result = type(
            "obj",
            (object,),
            {
                "original_text": "hello",
                "translated_text": "hola",
                "source_language": "EN",
                "target_language": "ES",
            },
        )()

        mock_service.translate = AsyncMock(return_value=mock_translation_result)
        mock_service_dep.return_value = mock_service

        response = client.post(
            "/api/v1/translate/",
            json={
                "text": "hello",
                "source_language": "EN",
                "target_language": "ES",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["original_text"] == "hello"
        assert data["translated_text"] == "hola"


def test_translate_batch(client):
    """Test batch translation endpoint."""
    with patch("app.api.dependencies.get_translation_service") as mock_service_dep:
        mock_service = AsyncMock()

        mock_result1 = type(
            "obj",
            (object,),
            {
                "original_text": "hello",
                "translated_text": "hola",
                "source_language": "EN",
                "target_language": "ES",
            },
        )()

        mock_result2 = type(
            "obj",
            (object,),
            {
                "original_text": "world",
                "translated_text": "mundo",
                "source_language": "EN",
                "target_language": "ES",
            },
        )()

        mock_service.translate_batch = AsyncMock(
            return_value=[mock_result1, mock_result2]
        )
        mock_service_dep.return_value = mock_service

        response = client.post(
            "/api/v1/translate/batch",
            json={
                "texts": ["hello", "world"],
                "source_language": "EN",
                "target_language": "ES",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "translations" in data
        assert len(data["translations"]) == 2


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
