from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass
class Bot:
    token: str


@dataclass
class Config:
    bot: Bot


def load_config(path: str | None = None) -> Config:
    load_dotenv(dotenv_path=path)
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    return Config(bot=bot)
