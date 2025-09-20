from dataclasses import dataclass

from dotenv import load_dotenv

from .base import getenv, ImproperlyConfigured


@dataclass
class TelegramBotConfig:
    token: str


@dataclass
class GeminiConfig:
    api_key: str


@dataclass
class Config:
    tg_bot: TelegramBotConfig
    gemini: GeminiConfig


def load_config() -> Config:
    # Parse a `.env` file and load the variables into environment valriables
    load_dotenv()

    return Config(
        tg_bot=TelegramBotConfig(token=getenv("BOT_TOKEN")),
        gemini=GeminiConfig(api_key=getenv("GEMINI_API_KEY"))
    )
