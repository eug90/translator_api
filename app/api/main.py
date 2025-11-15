from fastapi import FastAPI

from app.api.translation import router as translation_router

app = FastAPI(
    title="Translator API",
    description="A simple translation API service",
    version="0.1.0",
)

# Include the API routers
app.include_router(translation_router, prefix="/api/v1")
