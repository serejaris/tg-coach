import os
from dataclasses import dataclass


@dataclass
class Config:
    telegram_token: str
    database_url: str
    openrouter_api_key: str
    openrouter_model: str = "anthropic/claude-sonnet-4-20250514"
    admin_chat_id: int = 0
    morning_hour: int = 8
    timezone: str = "America/Argentina/Buenos_Aires"


def load_config() -> Config:
    return Config(
        telegram_token=os.environ["TELEGRAM_TOKEN"],
        database_url=os.environ["DATABASE_URL"],
        openrouter_api_key=os.environ["OPENROUTER_API_KEY"],
        openrouter_model=os.environ.get("OPENROUTER_MODEL", "anthropic/claude-sonnet-4-20250514"),
        admin_chat_id=int(os.environ.get("ADMIN_CHAT_ID", "0")),
        morning_hour=int(os.environ.get("MORNING_HOUR", "8")),
        timezone=os.environ.get("TIMEZONE", "America/Argentina/Buenos_Aires"),
    )
