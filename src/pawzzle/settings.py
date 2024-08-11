from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_connection_url: str = "sqlite:///:memory:"
    db_echo: bool = False
    dogs_file: str = ""
    origins: str = "http://localhost:3000"
    api_key: str = ""
    model_config = SettingsConfigDict(env_file=".env")
