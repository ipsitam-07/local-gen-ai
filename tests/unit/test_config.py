from app.core.config import Settings, get_settings


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.APP_NAME == "Local GenAI Data Assistant"
    assert settings.POSTGRES_PORT == 5432
    assert "postgresql+psycopg://" in settings.database_url
    assert "genai_reader" in settings.ro_database_url


def test_get_settings_caching() -> None:
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2
