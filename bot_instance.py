from aiogram import Bot
from localization import Localization

bot: Bot | None = None


def set_bot(new_bot: Bot):
    global bot
    bot = new_bot


def get_bot() -> Bot:
    if bot is None:
        raise ValueError(Localization.bot_not_initialized_error)
    return bot
