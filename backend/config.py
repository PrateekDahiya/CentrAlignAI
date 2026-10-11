"""Central config. Loads .env, no secrets in logs."""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    planner_model: str = os.getenv("PLANNER_MODEL", "openai/gpt-oss-120b")
    planner_fallback: str = os.getenv("PLANNER_FALLBACK", "qwen/qwen3.8-27b")
    executor_model: str = os.getenv("EXECUTOR_MODEL", "openai/gpt-oss-120b")
    executor_fallback: str = os.getenv("EXECUTOR_FALLBACK", "openai/gpt-oss-20b")
    verifier_model: str = os.getenv("VERIFIER_MODEL", "openai/gpt-oss-20b")
    max_steps: int = int(os.getenv("MAX_STEPS", "12"))
    db_host: str = os.getenv("DB_HOST", "")
    db_port: int = int(os.getenv("DB_PORT", "17886"))
    db_name: str = os.getenv("DB_NAME", "centralign")
    db_user: str = os.getenv("DB_USERNAME", "")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_ssl: bool = os.getenv("DB_SSL", "true").lower() == "true"


settings = Settings()
