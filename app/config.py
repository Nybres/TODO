from pathlib import Path

from pydantic_settings import SettingsConfigDict, BaseSettings

PROJECT_DIR = Path(__file__).resolve().parent.parent

_base_config = SettingsConfigDict(
    env_file=PROJECT_DIR / ".env",
    env_ignore_empty=True,
    extra="ignore",
)

class AppSettings(BaseSettings):
    APP_NAME: str = "TODO"
    APP_DOMAIN: str = "localhost:8000"


class DatabaseSettings(BaseSettings):
    model_config = _base_config

    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

class SecuritySettings(BaseSettings):
    model_config = _base_config

    JWT_SECRET: str
    JWT_ALGORITHM: str

app_settings = AppSettings()
db_settings = DatabaseSettings()
security_settings = SecuritySettings()