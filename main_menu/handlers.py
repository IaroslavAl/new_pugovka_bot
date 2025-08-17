from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from localization import Localization
from main_menu.keyboards import main_menu_keyboard
from main_menu.service import MenuService


main_menu_router = Router()
menu_service = MenuService()


@main_menu_router.message(CommandStart())
async def start_handler(message: Message):
    await message.delete()
    await menu_service.show_menu(
        chat_id=message.chat.id,
        text=Localization.MAIN_MENU_INRO,
        keyboard=main_menu_keyboard()
    )
