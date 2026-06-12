"""Production config — 12-Factor: tất cả từ environment variables."""
import os
from dataclasses import dataclass, field

@dataclass
class Settings:
    # Server
    host: str = field(default_factory=lambda: os.getenv("HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("PORT", "8000")))
    environment: str = field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")

    # App
    app_name: str = field(default_factory=lambda: os.getenv("APP_NAME", "Research Agent"))
    app_version: str = field(default_factory=lambda: os.getenv("APP_VERSION", "1.0.0"))

    # LLM
    provider_name: str = field(default_factory=lambda: os.getenv("PROVIDER_NAME", "openrouter"))
    model_name: str = field(default_factory=lambda: os.getenv("MODEL_NAME", "gpt-4o-mini"))

    # Security
    agent_api_key: str = field(default_factory=lambda: os.getenv("AGENT_API_KEY", "dev-key-change-me"))
    redis_url: str = field(default_factory=lambda: os.getenv("REDIS_URL", ""))

settings = Settings()
