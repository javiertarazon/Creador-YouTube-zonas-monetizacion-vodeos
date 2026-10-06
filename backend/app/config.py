from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    ollama_base_url: str = "http://ollama:11434"
    ollama_model: str = "llama3.2:3b"
    quality_min_score: float = 8.0
    target_lufs: int = -14
    youtube_auto_publish: bool = False
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
