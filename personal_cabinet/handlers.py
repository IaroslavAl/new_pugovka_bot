from aiogram import Router, F
from aiogram.types import CallbackQuery
from personal_cabinet.service import user_service
from personal_cabinet.models import PurchaseType
from personal_cabinet.keyboards import (
    personal_cabinet_main_keyboard,
    purchase_categories_keyboard,
    purchases_list_keyboard,
    purchase_detail_keyboard,
    empty_purchases_keyboard,
)
from main_menu.keyboards import main_menu_keyboard
from localization import Localization
from utils import safe_answer_callback, safe_edit_message

personal_cabinet_router = Router()


@personal_cabinet_router.callback_query(F.data == "section_personal")
async def personal_cabinet_main(callback: CallbackQuery):
    """Главная страница личного кабинета"""
    await safe_answer_callback(callback)

    user_id = callback.from_user.id
    user_service.get_or_create_user(
        user_id=user_id,
        username=callback.from_user.username or "",
        first_name=callback.from_user.first_name or "",
        last_name=callback.from_user.last_name or "",
    )

    await safe_edit_message(
        callback,
        text=Localization.personal_cabinet_intro,
        reply_markup=personal_cabinet_main_keyboard(),
        parse_mode="HTML",
    )


@personal_cabinet_router.callback_query(F.data.startswith("personal:"))
async def personal_cabinet_handler(callback: CallbackQuery):
    """Обработчик для всех действий в личном кабинете"""
    await safe_answer_callback(callback)

    user_id = callback.from_user.id
    data_parts = callback.data.split(":")

    if len(data_parts) < 2:
        return

    action = data_parts[1]

    # Возврат в главное меню личного кабинета
    if action == "back":
        await safe_edit_message(
            callback,
            text=Localization.personal_cabinet_intro,
            reply_markup=personal_cabinet_main_keyboard(),
            parse_mode="HTML",
        )
        return

    # Статистика покупок
    if action == "statistics":
        masterclasses = user_service.get_user_purchases_by_type(
            user_id, PurchaseType.masterclass
        )
        videocourses = user_service.get_user_purchases_by_type(
            user_id, PurchaseType.videocourse
        )
        patterns = user_service.get_user_purchases_by_type(
            user_id, PurchaseType.pattern
        )

        total_count = len(masterclasses) + len(videocourses) + len(patterns)

        statistics_text = Localization.personal_statistics.format(
            masterclasses_count=len(masterclasses),
            videocourses_count=len(videocourses),
            patterns_count=len(patterns),
            total_count=total_count,
        )

        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

        back_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=Localization.back_button, callback_data="personal:back"
                    )
                ]
            ]
        )

        await safe_edit_message(
            callback,
            text=statistics_text,
            reply_markup=back_keyboard,
            parse_mode="HTML",
        )
        return

    # Просмотр покупок по типам
    if action in ["masterclasses", "videocourses", "patterns"]:
        # Преобразуем множественное число в единственное для enum
        if action == "masterclasses":
            purchase_type = PurchaseType.masterclass
        elif action == "videocourses":
            purchase_type = PurchaseType.videocourse
        else:  # patterns
            purchase_type = PurchaseType.pattern
        categories = user_service.get_purchase_categories(user_id, purchase_type)

        if not categories:
            # Нет покупок этого типа
            if action == "masterclasses":
                text = Localization.personal_no_masterclasses
            elif action == "videocourses":
                text = Localization.personal_no_videocourses
            else:
                text = Localization.personal_no_patterns

            await safe_edit_message(
                callback,
                text=text,
                reply_markup=empty_purchases_keyboard(action),
                parse_mode="HTML",
            )
        else:
            # Показываем категории
            if action == "masterclasses":
                text = Localization.personal_masterclasses_title
            elif action == "videocourses":
                text = Localization.personal_videocourses_title
            else:
                text = Localization.personal_patterns_title

            await safe_edit_message(
                callback,
                text=text,
                reply_markup=purchase_categories_keyboard(categories, action),
                parse_mode="HTML",
            )
        return

    # Обработка выбора категории (новая схема с индексами)
    if len(data_parts) >= 4 and data_parts[2] == "cat":
        short_type = data_parts[1]
        category_index = int(data_parts[3])

        # Преобразуем сокращенные типы обратно в полные
        type_map = {"mc": "masterclasses", "vc": "videocourses", "pt": "patterns"}
        purchase_type_str = type_map.get(short_type, short_type)

        # Преобразуем в enum
        if purchase_type_str == "masterclasses":
            purchase_type = PurchaseType.masterclass
        elif purchase_type_str == "videocourses":
            purchase_type = PurchaseType.videocourse
        else:  # patterns
            purchase_type = PurchaseType.pattern

        # Получаем название категории по индексу
        category = user_service.get_category_by_index(
            user_id, purchase_type, category_index
        )
        if not category:
            return  # Неверный индекс

        purchases = user_service.get_purchases_by_category(
            user_id, purchase_type, category
        )

        text = Localization.personal_category_materials.format(category_name=category)

        await safe_edit_message(
            callback,
            text=text,
            reply_markup=purchases_list_keyboard(
                purchases, purchase_type_str, category_index
            ),
            parse_mode="HTML",
        )
        return

    # Обработка выбора конкретного товара
    if len(data_parts) >= 5 and data_parts[2] == "item":
        short_type = data_parts[1]
        item_index = int(data_parts[3])
        category_index = int(data_parts[4])

        # Преобразуем сокращенные типы обратно в полные
        type_map = {"mc": "masterclasses", "vc": "videocourses", "pt": "patterns"}
        purchase_type_str = type_map.get(short_type, short_type)

        # Преобразуем в enum
        if purchase_type_str == "masterclasses":
            purchase_type = PurchaseType.masterclass
        elif purchase_type_str == "videocourses":
            purchase_type = PurchaseType.videocourse
        else:  # patterns
            purchase_type = PurchaseType.pattern

        # Получаем категорию и товар по индексам
        category = user_service.get_category_by_index(
            user_id, purchase_type, category_index
        )
        if category:
            purchase = user_service.get_purchase_by_index_in_category(
                user_id, purchase_type, category, item_index
            )

            if purchase:
                # Формируем детальное описание
                detail_text = (
                    f"📝 <b>{purchase.title}</b>\n\n"
                    f"{Localization.item_description_label}\n{purchase.description}\n\n"
                    f"{Localization.item_category_label} {purchase.category}\n"
                    f"{Localization.item_purchase_date_label} {purchase.purchase_date}"
                )

                await safe_edit_message(
                    callback,
                    text=detail_text,
                    reply_markup=purchase_detail_keyboard(
                        purchase, purchase_type_str, category_index
                    ),
                    parse_mode="HTML",
                )
        return

    # Возврат из списка материалов к категориям
    if len(data_parts) >= 3 and data_parts[2] == "back":
        short_type = data_parts[1]

        # Преобразуем сокращенные типы обратно в полные
        type_map = {"mc": "masterclasses", "vc": "videocourses", "pt": "patterns"}
        purchase_type_str = type_map.get(short_type, short_type)

        # Преобразуем в enum
        if purchase_type_str == "masterclasses":
            purchase_type = PurchaseType.masterclass
        elif purchase_type_str == "videocourses":
            purchase_type = PurchaseType.videocourse
        else:  # patterns
            purchase_type = PurchaseType.pattern

        categories = user_service.get_purchase_categories(user_id, purchase_type)

        if purchase_type_str == "masterclasses":
            text = Localization.personal_masterclasses_title
        elif purchase_type_str == "videocourses":
            text = Localization.personal_videocourses_title
        else:
            text = Localization.personal_patterns_title

        await safe_edit_message(
            callback,
            text=text,
            reply_markup=purchase_categories_keyboard(categories, purchase_type_str),
            parse_mode="HTML",
        )
        return


@personal_cabinet_router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(callback: CallbackQuery):
    """Возврат в главное меню"""
    await safe_answer_callback(callback)

    await safe_edit_message(
        callback,
        text=Localization.main_menu_intro,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
