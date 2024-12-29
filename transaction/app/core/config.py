# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MongoDB settings
    MONGO_URI: str = "mongodb+srv://root:admin@cluster0.buv7v.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    PORT: int = 8000
    MONGODB_MAX_POOL_SIZE: int = 100
    MONGODB_MIN_POOL_SIZE: int = 10
    MONGODB_TIMEOUT_MS: int = 5000
    
    # Application settings
    ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    APP_NAME: str = "banking-transaction-service"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()