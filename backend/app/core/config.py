from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    MAX_RETRIES: int = 2

    class Config:
        env_file = ".env"

settings = Settings()
