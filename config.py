from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    gemini_api_key: str = Field("", env="GEMINI_API_KEY")
    claude_api_key: str = Field("", env="CLAUDE_API_KEY")

settings = Settings()
