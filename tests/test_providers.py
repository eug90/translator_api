from unittest.mock import AsyncMock, patch

import pytest

from app.core.providers.deepl import DeepLProvider


@pytest.fixture
def deepl_provider():
    """Create a DeepL provider instance for testing."""
    return DeepLProvider(api_url="test.url", api_key="test-key")


def test_is_language_supported(deepl_provider):
    """Test language support checking."""
    assert deepl_provider.is_language_supported("EN") is True
    assert deepl_provider.is_language_supported("ES") is True
    assert deepl_provider.is_language_supported("FR") is True
    assert deepl_provider.is_language_supported("DE") is False
    assert deepl_provider.is_language_supported("AUTO") is True


def test_get_supported_languages(deepl_provider):
    """Test getting list of supported languages."""
    languages = deepl_provider.get_supported_languages()
    assert len(languages) == 3
    assert any(lang.code == "EN" for lang in languages)
    assert any(lang.code == "ES" for lang in languages)
    assert any(lang.code == "FR" for lang in languages)


@pytest.mark.asyncio
async def test_translate_unsupported_target_language(deepl_provider):
    """Test translation with unsupported target language."""
    with pytest.raises(ValueError, match="Target language 'DE' is not supported"):
        await deepl_provider.translate("hello", "EN", "DE")


@pytest.mark.asyncio
async def test_translate_unsupported_source_language(deepl_provider):
    """Test translation with unsupported source language."""
    with pytest.raises(ValueError, match="Source language 'DE' is not supported"):
        await deepl_provider.translate("hello", "DE", "EN")


@pytest.mark.asyncio
async def test_translate_batch_unsupported_language(deepl_provider):
    """Test batch translation with unsupported language."""
    with pytest.raises(ValueError, match="Target language 'DE' is not supported"):
        await deepl_provider.translate_batch(["hello", "world"], "EN", "DE")


@pytest.mark.asyncio
async def test_translate_with_retry_success(deepl_provider):
    """Test translation with retry mechanism succeeds."""
    mock_response = {"translations": [{"text": "hola"}]}

    with patch(
        "app.core.providers.deepl.call_remote_api", new_callable=AsyncMock
    ) as mock_call:
        mock_call.return_value = mock_response

        result = await deepl_provider.translate("hello", "EN", "ES")
        assert result == "hola"
        mock_call.assert_called_once()


@pytest.mark.asyncio
async def test_translate_with_retry_failure(deepl_provider):
    """Test translation with retry mechanism fails after max retries."""
    deepl_provider.max_retries = 2
    deepl_provider.retry_delay = 0.01

    with patch(
        "app.core.providers.deepl.call_remote_api", new_callable=AsyncMock
    ) as mock_call:
        mock_call.side_effect = Exception("API Error")

        with pytest.raises(Exception, match="Translation failed after 2 retries"):
            await deepl_provider.translate("hello", "EN", "ES")

        assert mock_call.call_count == 2


@pytest.mark.asyncio
async def test_translate_batch(deepl_provider):
    """Test batch translation."""
    mock_response = {"translations": [{"text": "hola"}]}

    with patch(
        "app.core.providers.deepl.call_remote_api", new_callable=AsyncMock
    ) as mock_call:
        mock_call.return_value = mock_response

        results = await deepl_provider.translate_batch(["hello", "world"], "EN", "ES")
        assert len(results) == 2
