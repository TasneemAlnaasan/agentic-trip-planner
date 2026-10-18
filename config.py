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


def get_settings():
    """
    If running on Streamlit Cloud, read from st.secrets.
    Otherwise (locally in Codespaces), fall back to reading from .env.
    """
    try:
        import streamlit as st
        if hasattr(st, "secrets") and len(st.secrets) > 0:
            return Settings(
                tavily_api_key=st.secrets.get("TAVILY_API_KEY", ""),
                groq_api_key=st.secrets.get("GROQ_API_KEY", ""),
                geoapify_api_key=st.secrets.get("GEOAPIFY_API_KEY", ""),
                max_attempts=int(st.secrets.get("MAX_ATTEMPTS", 3)),
            )
    except Exception:
        pass

    return Settings()


settings = get_settings()