from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):

    APP_NAME: str = "Document RAG Assistant"

    APP_VERSION: str = "1.0.0"

    UPLOAD_DIRECTORY: str = "data/uploads"

    PROCESSED_DIRECTORY: str = "data/processed"

    VECTOR_DB_DIRECTORY: str = "data/vector_db"

    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()