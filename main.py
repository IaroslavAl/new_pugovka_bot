import asyncio
from aiogram import Bot, Dispatcher
from config import Config, load_config


async def main():
    config: Config = load_config()
    bot = Bot(token=config.bot.token)
    dp = Dispatcher()

    # TODO: register routers

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
