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
    materials: list[dict], section_type: str, user_purchases: list[str] = None
) -> InlineKeyboardMarkup:
    """Клавиатура с материалами, показывающая статус покупки"""
    if user_purchases is None:
        user_purchases = []

    keyboard = []
    for material in materials:
        item_id = material["id"]
        title = material["title"]

        # Обрезаем длинные названия
        if len(title) > 25:
            title = title[:22] + "..."

        # Создаем кнопку с информацией о покупке
        if item_id in user_purchases:
            # Товар куплен - показываем кнопку с иконкой покупки, но всё ещё открываем детали
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=f"📖 {title}",
                        callback_data=f"item_details:{section_type}:{item_id}",
                    )
                ]
            )
        else:
            # Товар не куплен - показываем кнопку "Подробнее"
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=f"📋 {title}",
                        callback_data=f"item_details:{section_type}:{item_id}",
                    )
                ]
            )

    keyboard.append(
        [
            InlineKeyboardButton(
                text=Localization.back_button, callback_data=f"{section_type}:back"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def item_details_keyboard(
    item_id: str, section_type: str, is_purchased: bool, category: str = ""
) -> InlineKeyboardMarkup:
    """Клавиатура для страницы деталей товара"""
    keyboard = []

    if is_purchased:
        # Товар куплен - кнопка "Открыть"
        # Получаем ссылку из данных товара
        from content_section.data import masterclasses, videocourses, patterns

        item_data = None
        if section_type == "masterclasses":
            item_data = masterclasses.get(item_id)
        elif section_type == "videocourses":
            item_data = videocourses.get(item_id)
        elif section_type == "patterns":
            item_data = patterns.get(item_id)

        if item_data:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=Localization.open_button, url=item_data["link"]
                    )
                ]
            )
    else:
        # Товар не куплен - кнопка "Купить"
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=Localization.buy_button,
                    callback_data=f"purchase:{section_type}:{item_id}",
                )
            ]
        )

    # Кнопка "Назад"
    back_callback = (
        f"{section_type}:back_to_category:{category}"
        if category
        else f"{section_type}:back"
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                text=Localization.back_button,
                callback_data=back_callback,
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
