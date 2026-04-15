from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    APP_NAME: str = "Matos Backend"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "INFO"
    
    CORS_ORIGINS: list[str] = ["*"]

    DATABASE_URL: str = "src/data/matos.db"
    PRODUCTS_FILE: str = "src/data/products.json"


settings = Settings()
