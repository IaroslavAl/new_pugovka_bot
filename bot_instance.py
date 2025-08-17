from aiogram import Bot

bot: Bot | None = None


def set_bot(new_bot: Bot):
    global bot
    bot = new_bot


def get_bot() -> Bot:
    if bot is None:
        raise ValueError("Bot не инициализирован")
    return bot
