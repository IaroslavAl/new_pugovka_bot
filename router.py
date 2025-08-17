from aiogram import Dispatcher
from main_menu.handlers import main_menu_router
from content_section.handlers import content_section_router


def register_routers(dispatcher: Dispatcher):
    dispatcher.include_router(content_section_router)
    dispatcher.include_router(main_menu_router)
