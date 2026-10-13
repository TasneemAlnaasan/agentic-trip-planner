from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API keys
    tavily_api_key: str = ""
    groq_api_key: str = ""
    geoapify_api_key: str = ""

    # max number of replanning attempts in the loop
    max_attempts: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
