# Translation API - Production Ready

> A comprehensive translation service built with FastAPI, featuring DeepL provider, intelligent caching, automatic retries, and batch translation support.

## ⭐ Features

- **Single & Batch Translation** - Translate one or many texts efficiently
- **DeepL Provider** - Uses DeepL API with automatic retries
- **Smart Caching** - Transparent in-memory caching of translations
- **Retry Mechanism** - Automatic retries for transient failures
- **Asynchronous** - Build upon AsyncIO
- **Type Safe** - Full type hints with Pydantic validation

## 🚀 Quick Start

### 1. Install Dependencies
```bash
uv sync
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your DeepL API key
```

### 3. Run the Server
```bash
uvicorn app.api.main:app --reload
```

### 4. Access the API
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 5. Run Tests
```bash
pytest
```

## 📖 API Endpoints

### Get Supported Languages
```bash
GET /api/v1/translate/languages
```

### Translate Single Text
```bash
POST /api/v1/translate/
Content-Type: application/json

{
  "text": "Hello, world!",
  "source_language": "EN",
  "target_language": "ES"
}
```

### Translate Multiple Texts
```bash
POST /api/v1/translate/batch
Content-Type: application/json

{
  "texts": ["Hello", "World", "How are you?"],
  "source_language": "EN",
  "target_language": "ES"
}
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_service.py

# Run with coverage
pytest --cov=app --cov-report=html
```

### Add New Languages
Update `SUPPORTED_LANGUAGES` in `app/core/providers/deepl.py`.

## 📋 Supported Languages

- 🇬🇧 English (EN)
- 🇪🇸 Spanish (ES)
- 🇫🇷 French (FR)

## 🎯 Key Features

### Batch Optimization
- Checks cache for each text
- Groups uncached texts
- Single API call for batch

### Retry Mechanism
- Default 3 retries
- 1 second delay between retries

## 🔐 Configuration

### Required Environment Variables
```
DEEPL_API_KEY=your-deepl-api-key
```

## 📝 API Response Format

### Success Response
```json
{
  "original_text": "Hello, world!",
  "translated_text": "¡Hola, mundo!",
  "source_language": "EN",
  "target_language": "ES"
}
```

### Error Response
```json
{
  "detail": "Target language 'XX' is not supported"
}
```

## 📦 Dependencies

### Main
- **fastapi** - Web framework
- **httpx** - Async HTTP client
- **pydantic** - Data validation
- **python-dotenv** - Environment management

### Dev
- **pytest** - Testing framework
- **pytest-asyncio** - Async test support
- **mypy** - Type checker
- **ruff** - Linter

## 📄 License

MIT

---

**Status**: ✅ Production Ready

All requirements implemented, tested, and documented.
