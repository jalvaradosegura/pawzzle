from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_connection_url: str = "sqlite:///:memory:"
    model_config = SettingsConfigDict(env_file=".env")
