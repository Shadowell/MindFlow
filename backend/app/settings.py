from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class ConfigurationError(RuntimeError):
    """Raised when required runtime configuration is missing."""


class BackendSettings(BaseSettings):
    app_env: str = "development"
    database_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=str(REPO_ROOT / ".env"),
        extra="ignore",
        populate_by_name=True,
    )

    def require_database_url(self) -> str:
        if not self.database_url:
            raise ConfigurationError(
                "DATABASE_URL is required for database-backed backend operations."
            )
        return self.database_url
