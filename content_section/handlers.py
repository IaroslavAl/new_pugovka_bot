from aiogram import Router, F
from aiogram.types import CallbackQuery
from content_section.service import ContentService
from content_section.keyboards import category_keyboard, materials_keyboard
from content_section.data import masterclasses, videocourses, patterns
from main_menu.keyboards import main_menu_keyboard
from main_menu.models import Section
from localization import Localization

content_section_router = Router()

services = {
    Section.masterclasses: ContentService(masterclasses),
    Section.videocourses: ContentService(videocourses),
    Section.patterns: ContentService(patterns),
}


@content_section_router.callback_query(F.data.startswith(tuple(Section)))
async def section_handler(callback: CallbackQuery):
    await callback.answer()

    data_parts = callback.data.split(":", 1)
    section_type = Section(data_parts[0])
    action = data_parts[1] if len(data_parts) > 1 else None

    service = services[section_type]

    if action == "back":
        categories = service.get_categories()
        await callback.message.edit_text(
            text=Localization.prompt_choose_category,
            reply_markup=category_keyboard(categories, section_type),
            parse_mode="HTML",
        )
    elif action is not None and action.startswith("category"):
        category_name = action.split("category:")[-1]
        materials = service.get_materials_by_category(category_name)
        await callback.message.edit_text(
            text=Localization.prompt_category_materials.format(
                category_name=category_name
            ),
            reply_markup=materials_keyboard(materials, section_type),
            parse_mode="HTML",
        )


@content_section_router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        text=Localization.main_menu_intro,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
