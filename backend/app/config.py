from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/api_pilot.db"

    # Auth
    API_PILOT_SECRET_KEY: str = "dev-secret-key-change-in-production"
    API_PILOT_ALGORITHM: str = "HS256"
    API_PILOT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # CORS
    CORS_ORIGINS: str = "http://localhost:8080,http://localhost:8081"

    # Cloudflare Turnstile
    TURNSTILE_SECRET_KEY: str = ""

    # Environment
    ENV: str = "development"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()