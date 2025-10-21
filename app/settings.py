from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    env: str = "dev"
    cors_origins: list[str] = ["*"]
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
