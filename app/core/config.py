from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses Pydantic BaseSettings for type-safe configuration.
    """

    deepl_api_key: str = Field(default="", alias="DEEPL_API_KEY")
    deepl_api_url: str = Field(
        default="https://api-free.deepl.com/v2/translate", alias="DEEPL_API_URL"
    )

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create a singleton instance
settings = Settings()
