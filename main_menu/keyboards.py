from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main_menu.models import Buttons


def main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=button.value,
                callback_data=button.name,
            )
        ]
        for button in Buttons
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
