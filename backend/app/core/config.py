import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Root directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "Legal Predictor API"
    ENVIRONMENT: str = "development"
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    
    # Path settings
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_CLEAN_DIR: Path = DATA_DIR / "raw" / "clean"
    RAW_PROB_DIR: Path = DATA_DIR / "raw" / "prob"
    PROCESSED_DIR: Path = DATA_DIR / "processed"
    REFERENCE_DIR: Path = DATA_DIR / "reference"
    VECTOR_DB_DIR: Path = DATA_DIR / "vector_db"
    
    # Embedding Model & Vector DB
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    VECTOR_COLLECTION_NAME: str = "legal_benchmark_clauses"
    TOP_K_RESULTS: int = 3
    
    # Gemini API Key (for LLM Reasoner)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_NAME: str = "gemini-2.5-flash"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
