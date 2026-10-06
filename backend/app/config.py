from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-6-luna"
    model_timeout_seconds: int = 180
    youtube_api_key: str = ""
    youtube_trend_results: int = 10
    quality_min_score: float = 8.0
    target_lufs: int = -14
    youtube_auto_publish: bool = False
    piper_model: str = ""
    piper_command: str = "piper"
    output_dir: str = "output"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
