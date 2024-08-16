from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_connection_url: str = "sqlite:///:memory:"
    db_echo: bool = False
    dogs_file: str = ""
    origins: str = "http://localhost:3000"
    api_key: str = ""

    sentry_dns: str = ""
    sentry_environment: str = "local"
    sentry_traces_sample_rate: float = 0.1
    sentry_profiles_sample_rate: float = 0.05

    model_config = SettingsConfigDict(env_file=".env")
