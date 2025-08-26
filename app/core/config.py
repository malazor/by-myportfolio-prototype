from pydantic_settings import BaseSettings, SettingsConfigDict

# TODO: Evaluar si esta clase merece la pena
class Settings(BaseSettings):
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Opcionales
    JWT_ISSUER: str | None = None
    JWT_AUDIENCE: str | None = None

    # App
    APP_NAME: str = "FinAPI"
    APP_ENV: str = "dev"
    BACKEND_CORS_ORIGINS: str = "http://localhost:8000"

    # DDBB
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
