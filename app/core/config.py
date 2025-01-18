from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Project"
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
