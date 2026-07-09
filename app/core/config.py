from pathlib import Path
from pydantic_settings import BaseSettings,SettingsConfigDict

ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str

    EMBEDDING_MODEL: str

    CHUNK_SIZE: int
    CHUNK_OVERLAP: int

    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION: str
    EMBEDDING_DIMENSION: int
    TOP_K: int
    
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str | None = None
  
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        extra="ignore"
    )
settings = Settings()