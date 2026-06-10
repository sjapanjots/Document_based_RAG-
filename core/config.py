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

    GEMINI_MODEL: str = "gemini-1.5-flash"

    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

    EMBEDDING_DIMENSION: int = 384

    CHUNK_SIZE: int = 900

    CHUNK_OVERLAP: int = 150

    TOP_K: int = 4

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
