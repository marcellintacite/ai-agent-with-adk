from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    APP_NAME: str = "Matos WhatsApp Bridge"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "INFO"
    
    # ADK Agent Config
    # Format: https://SERVICE_NAME-PROJECT_ID.REGION.run.app
    ADK_SERVICE_URL: str = "https://matos-agent-service-742494222209.us-central1.run.app"
    ADK_APP_NAME: str = "matos"
    
    # Twilio Config
    TWILIO_ACCOUNT_SID: str | None = None
    TWILIO_AUTH_TOKEN: str | None = None
    TWILIO_FROM_NUMBER: str = "whatsapp:+14155238886"
    OWNER_PHONE: str = "whatsapp:+243999537410"

    PORT: int = 8080


settings = Settings()
