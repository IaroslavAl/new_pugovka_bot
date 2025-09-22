from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
from personal_cabinet.models import Purchase
from localization import Localization


def personal_cabinet_main_keyboard() -> InlineKeyboardMarkup:
    """Главная клавиатура личного кабинета"""
    keyboard = [
        [
            InlineKeyboardButton(
                text=Localization.personal_my_masterclasses_button,
                callback_data="personal:masterclasses",
            )
        ],
        [
            InlineKeyboardButton(
                text=Localization.personal_my_videocourses_button,
                callback_data="personal:videocourses",
            )
        ],
        [
            InlineKeyboardButton(
                text=Localization.personal_my_patterns_button,
                callback_data="personal:patterns",
            )
        ],
        [
            InlineKeyboardButton(
                text=Localization.personal_statistics_button,
                callback_data="personal:statistics",
            )
        ],
        [
            InlineKeyboardButton(
                text=Localization.back_to_main_menu_button,
                callback_data="back_to_main_menu",
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def purchase_categories_keyboard(
    categories: List[str], purchase_type: str
) -> InlineKeyboardMarkup:
    """Клавиатура для выбора категории покупок"""
    keyboard = []

    # Сокращаем purchase_type для экономии места в callback_data
    type_map = {"masterclasses": "mc", "videocourses": "vc", "patterns": "pt"}
    short_type = type_map.get(purchase_type, purchase_type)

    for i, category in enumerate(categories):
        # Используем индекс вместо полного названия категории
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=category,
                    callback_data=f"personal:{short_type}:cat:{i}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text=Localization.back_button, callback_data="personal:back"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def purchases_list_keyboard(
    purchases: List[Purchase], purchase_type: str, category_index: int = 0
) -> InlineKeyboardMarkup:
    """Клавиатура со списком покупок"""
    keyboard = []

    # Сокращения типов для callback_data
    type_map = {"masterclasses": "mc", "videocourses": "vc", "patterns": "pt"}
    short_type = type_map.get(purchase_type, purchase_type)

    for i, purchase in enumerate(purchases):
        # Обрезаем длинные названия для красивого отображения
        title = purchase.title
        if len(title) > 30:
            title = title[:27] + "..."

        # Используем callback_data для показа деталей товара
        # Включаем category_index для правильной навигации назад
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=title,
                    callback_data=f"personal:{short_type}:item:{i}:{category_index}",
                )
            ]
        )

    # Добавляем кнопку "Назад"
    keyboard.append(
        [
            InlineKeyboardButton(
                text=Localization.back_button,
                callback_data=f"personal:{short_type}:back",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def purchase_detail_keyboard(
    purchase: Purchase, purchase_type: str, category_index: int
) -> InlineKeyboardMarkup:
    """Клавиатура для детального просмотра покупки"""
    # Сокращения типов для callback_data
    type_map = {"masterclasses": "mc", "videocourses": "vc", "patterns": "pt"}
    short_type = type_map.get(purchase_type, purchase_type)

    keyboard = [
        [
            InlineKeyboardButton(
                text=Localization.open_material_button, url=purchase.link
            )
        ],
        [
            InlineKeyboardButton(
                text=Localization.back_to_list_button,
                callback_data=f"personal:{short_type}:cat:{category_index}",
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def empty_purchases_keyboard(purchase_type: str) -> InlineKeyboardMarkup:
    """Клавиатура для пустого списка покупок"""
    keyboard = [
        [
            InlineKeyboardButton(
                text=Localization.go_to_purchases_button,
                callback_data="back_to_main_menu",
            )
        ],
        [
            InlineKeyboardButton(
                text=Localization.back_button, callback_data="personal:back"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
