from aiogram import Dispatcher
from main_menu.handlers import main_menu_router


def register_routers(dispatcher: Dispatcher):
    dispatcher.include_router(main_menu_router)
