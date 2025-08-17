import asyncio
from aiogram import Bot, Dispatcher
from config import Config, load_config
from router import register_routers
from bot_instance import set_bot


async def main():
    config: Config = load_config()

    bot = Bot(token=config.bot.token)
    set_bot(bot)

    dispatcher = Dispatcher()
    register_routers(dispatcher=dispatcher)

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
