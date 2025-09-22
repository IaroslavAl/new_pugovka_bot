"""
Вспомогательные функции для бота
"""

import logging
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

logger = logging.getLogger(__name__)


async def safe_answer_callback(
    callback: CallbackQuery, text: str = "", show_alert: bool = False
):
    """
    Безопасный ответ на callback запрос с обработкой исключений
    """
    try:
        await callback.answer(text=text, show_alert=show_alert)
    except TelegramBadRequest as e:
        if "query is too old" in str(e) or "query ID is invalid" in str(e):
            logger.warning(f"Callback query expired or invalid: {e}")
            # Не прерываем выполнение, просто логируем
            pass
        else:
            # Если это другая ошибка, перебрасываем её
            raise e
    except Exception as e:
        logger.error(f"Unexpected error in callback answer: {e}")
        # Не прерываем выполнение для других ошибок тоже
        pass


async def safe_edit_message(
    callback: CallbackQuery, text: str, reply_markup=None, parse_mode: str = None
):
    """
    Безопасное редактирование сообщения с обработкой исключений
    """
    try:
        await callback.message.edit_text(
            text=text, reply_markup=reply_markup, parse_mode=parse_mode
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            logger.warning(f"Message content unchanged: {e}")
            # Просто игнорируем, если сообщение не изменилось
            return
        elif "BUTTON_DATA_INVALID" in str(e):
            logger.error(f"Invalid button data: {e}")
            # Попробуем отправить сообщение без клавиатуры
            try:
                await callback.message.edit_text(text=text, parse_mode=parse_mode)
            except Exception:
                pass
        else:
            logger.error(f"Telegram error in message edit: {e}")
            raise e
    except Exception as e:
        logger.error(f"Unexpected error in message edit: {e}")
        raise e
