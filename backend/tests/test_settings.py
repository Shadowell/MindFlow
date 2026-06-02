import pytest

from app.settings import BackendSettings, ConfigurationError


def test_require_database_url_raises_clear_error_when_missing() -> None:
    settings = BackendSettings(app_env="test", database_url=None)

    with pytest.raises(ConfigurationError) as exc_info:
        settings.require_database_url()

    assert "DATABASE_URL is required" in str(exc_info.value)


def test_require_database_url_returns_configured_value() -> None:
    settings = BackendSettings(
        app_env="test",
        database_url="postgresql+psycopg://mindflow:secret@localhost:5432/mindflow",
    )

    assert (
        settings.require_database_url()
        == "postgresql+psycopg://mindflow:secret@localhost:5432/mindflow"
    )
