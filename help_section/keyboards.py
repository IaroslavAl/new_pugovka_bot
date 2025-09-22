from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from help_section.models import HelpSection
from localization import Localization


def help_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=Localization.help_faq_button,
                callback_data=f"help_{HelpSection.faq}",
            )
        ],
        [
            InlineKeyboardButton(
                text=Localization.help_instructions_button,
                callback_data=f"help_{HelpSection.instructions}",
            )
        ],
        [
            InlineKeyboardButton(
                text=Localization.help_contact_button,
                callback_data=f"help_{HelpSection.contact}",
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


def faq_keyboard(faq_items: list) -> InlineKeyboardMarkup:
    keyboard = []

    # Добавляем кнопки для каждого FAQ
    for i, item in enumerate(faq_items):
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"❓ {item.question[:50]}{'...' if len(item.question) > 50 else ''}",
                    callback_data=f"faq_item_{i}",
                )
            ]
        )

    # Кнопка "Назад"
    keyboard.append(
        [InlineKeyboardButton(text=Localization.back_button, callback_data="help_back")]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def faq_detail_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=Localization.back_button, callback_data="faq_back")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
