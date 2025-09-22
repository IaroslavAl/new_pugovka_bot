from aiogram import Router, F
from aiogram.types import CallbackQuery
from content_section.service import ContentService
from content_section.keyboards import (
    category_keyboard,
    materials_keyboard,
    item_details_keyboard,
)
from content_section.data import masterclasses, videocourses, patterns
from main_menu.keyboards import main_menu_keyboard
from main_menu.models import Section
from personal_cabinet.service import user_service
from personal_cabinet.models import PurchaseType
from localization import Localization
from utils import safe_answer_callback

content_section_router = Router()

services = {
    Section.masterclasses: ContentService(masterclasses),
    Section.videocourses: ContentService(videocourses),
    Section.patterns: ContentService(patterns),
}


@content_section_router.callback_query(F.data.startswith(tuple(Section)))
async def section_handler(callback: CallbackQuery):
    await safe_answer_callback(callback)

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
    elif action is not None and action.startswith("back_to_category"):
        # Обрабатываем возврат к списку материалов категории
        category_name = action.split("back_to_category:")[-1]
        materials = service.get_materials_by_category(category_name)

        # Получаем список покупок пользователя
        user_id = callback.from_user.id
        user_purchases = user_service.get_user_purchases(user_id)
        purchased_ids = [p.id for p in user_purchases]

        await callback.message.edit_text(
            text=Localization.prompt_category_materials.format(
                category_name=category_name
            ),
            reply_markup=materials_keyboard(materials, section_type, purchased_ids),
            parse_mode="HTML",
        )
    elif action is not None and action.startswith("category"):
        category_name = action.split("category:")[-1]
        materials = service.get_materials_by_category(category_name)

        # Получаем список покупок пользователя
        user_id = callback.from_user.id
        user_purchases = user_service.get_user_purchases(user_id)
        purchased_ids = [p.id for p in user_purchases]

        await callback.message.edit_text(
            text=Localization.prompt_category_materials.format(
                category_name=category_name
            ),
            reply_markup=materials_keyboard(materials, section_type, purchased_ids),
            parse_mode="HTML",
        )


@content_section_router.callback_query(F.data.startswith("item_details:"))
async def item_details_handler(callback: CallbackQuery):
    """Обработчик для показа деталей товара"""
    await safe_answer_callback(callback)

    data_parts = callback.data.split(":")
    if len(data_parts) < 3:
        return

    section_type = data_parts[1]
    item_id = data_parts[2]
    user_id = callback.from_user.id

    # Получаем данные товара
    if section_type == "masterclasses":
        item_data = masterclasses.get(item_id)
        item_type = Localization.item_type_masterclass
    elif section_type == "videocourses":
        item_data = videocourses.get(item_id)
        item_type = Localization.item_type_videocourse
    elif section_type == "patterns":
        item_data = patterns.get(item_id)
        item_type = Localization.item_type_pattern
    else:
        return

    if not item_data:
        return

    # Проверяем, куплен ли товар
    user_purchases = user_service.get_user_purchases(user_id)
    is_purchased = any(p.id == item_id for p in user_purchases)

    # Формируем текст с деталями
    status = (
        Localization.item_status_purchased
        if is_purchased
        else Localization.item_status_available
    )
    text = (
        f"📋 <b>{item_data['title']}</b>\n\n"
        f"{Localization.item_description_label}\n{item_data['description']}\n\n"
        f"{Localization.item_category_label} {item_data['category']}\n"
        f"{Localization.item_status_label} {status}\n\n"
        f"{Localization.item_help_text.format(item_type=item_type)}"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=item_details_keyboard(
            item_id, section_type, is_purchased, item_data["category"]
        ),
        parse_mode="HTML",
    )


@content_section_router.callback_query(F.data.startswith("purchase:"))
async def purchase_handler(callback: CallbackQuery):
    """Обработчик покупки товара"""
    await safe_answer_callback(callback)

    data_parts = callback.data.split(":")
    if len(data_parts) < 3:
        return

    section_type = data_parts[1]
    item_id = data_parts[2]
    user_id = callback.from_user.id

    # Определяем тип покупки
    if section_type == "masterclasses":
        purchase_type = PurchaseType.masterclass
        item_data = masterclasses.get(item_id)
    elif section_type == "videocourses":
        purchase_type = PurchaseType.videocourse
        item_data = videocourses.get(item_id)
    elif section_type == "patterns":
        purchase_type = PurchaseType.pattern
        item_data = patterns.get(item_id)
    else:
        return

    if not item_data:
        await callback.message.answer(Localization.purchase_error)
        return

    # Совершаем покупку
    success = user_service.add_purchase(user_id, item_id, purchase_type)

    if success:
        # Покупка успешна
        text = Localization.purchase_success.format(item_title=item_data["title"])

        # Обновляем клавиатуру на "Открыть"
        keyboard = item_details_keyboard(
            item_id, section_type, True, item_data["category"]
        )

        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    else:
        # Товар уже куплен
        await callback.message.answer(Localization.purchase_already_owned)


@content_section_router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(callback: CallbackQuery):
    await safe_answer_callback(callback)

    await callback.message.edit_text(
        text=Localization.main_menu_intro,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
