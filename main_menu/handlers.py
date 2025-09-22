from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from main_menu.service import MenuService
from main_menu.keyboards import main_menu_keyboard
from main_menu.models import Section
from content_section.service import ContentService
from content_section.keyboards import category_keyboard
from content_section.data import masterclasses, videocourses, patterns
from localization import Localization
from utils import safe_answer_callback

main_menu_router = Router()
menu_service = MenuService()

services = {
    Section.masterclasses: ContentService(masterclasses),
    Section.videocourses: ContentService(videocourses),
    Section.patterns: ContentService(patterns),
}


@main_menu_router.message(CommandStart())
async def start_handler(message: Message):
    await menu_service.show_menu(
        chat_id=message.chat.id,
        text=Localization.main_menu_intro,
        keyboard=main_menu_keyboard(),
    )


@main_menu_router.callback_query(
    F.data.in_([f"section_{s}" for s in Section if s != "support"])
)
async def main_menu_callback(callback: CallbackQuery):
    await safe_answer_callback(callback)

    section_type = callback.data.replace("section_", "")
    service = services[Section(section_type)]

    categories = service.get_categories()
    await callback.message.edit_text(
        text=Localization.prompt_choose_category,
        reply_markup=category_keyboard(categories, section_type),
        parse_mode="HTML",
    )
