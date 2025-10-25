from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/hello")
async def hello():
    """Simple hello endpoint for health checks."""
    return {"message": "Hello from Translator API!"}


@router.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Translator API"}
