from typing import List, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Uzaii Develop By North's"
    app_env: str = "development"
    app_version: str = "0.1.0"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "change-me-to-a-secure-32-character-secret-key-in-production"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/uzaii"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: Union[str, List[str]] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:8000",
        "http://127.0.0.1:8008",
        "*"
    ]

    real_send: bool = False
    ai_enabled: bool = True
    discovery_enabled: bool = True
    outreach_enabled: bool = True
    messaging_enabled: bool = False
    workers_enabled: bool = True

    @field_validator("cors_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, (list, str)):
            return v  # type: ignore[return-value]
        raise ValueError(v)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
