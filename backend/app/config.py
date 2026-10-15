from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "BookFlow API"
    database_url: str = "postgresql+psycopg://bookflow:bookflow@localhost:5432/bookflow"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
