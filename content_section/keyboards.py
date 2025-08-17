from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from localization import Localization


def category_keyboard(categories: list[str], section_type: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=category, callback_data=f"{section_type}:category:{category}"
            )
        ]
        for category in categories
    ]
    keyboard.append(
        [
            InlineKeyboardButton(
                text=Localization.back_button, callback_data="back_to_main_menu"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def materials_keyboard(
    materials: list[dict], section_type: str
) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=matireal["title"], url=matireal["link"])]
        for matireal in materials
    ]
    keyboard.append(
        [
            InlineKeyboardButton(
                text=Localization.back_button, callback_data=f"{section_type}:back"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
