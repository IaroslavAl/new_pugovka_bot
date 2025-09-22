from aiogram import Router, F
from aiogram.types import CallbackQuery
from help_section.service import HelpService
from help_section.keyboards import help_main_keyboard, faq_keyboard, faq_detail_keyboard
from help_section.models import HelpSection
from localization import Localization
from utils import safe_answer_callback

help_section_router = Router()
help_service = HelpService()


@help_section_router.callback_query(F.data == "section_support")
async def help_main_handler(callback: CallbackQuery):
    """Главное меню раздела помощи"""
    await safe_answer_callback(callback)

    await callback.message.edit_text(
        text=Localization.help_main_intro,
        reply_markup=help_main_keyboard(),
        parse_mode="HTML",
    )


@help_section_router.callback_query(F.data == "help_back")
async def help_back_handler(callback: CallbackQuery):
    """Возврат в главное меню помощи"""
    await safe_answer_callback(callback)

    await callback.message.edit_text(
        text=Localization.help_main_intro,
        reply_markup=help_main_keyboard(),
        parse_mode="HTML",
    )


@help_section_router.callback_query(F.data == f"help_{HelpSection.faq}")
async def faq_handler(callback: CallbackQuery):
    """Список часто задаваемых вопросов"""
    await safe_answer_callback(callback)

    faq_items = help_service.get_faq_items()

    await callback.message.edit_text(
        text=Localization.help_faq_intro,
        reply_markup=faq_keyboard(faq_items),
        parse_mode="HTML",
    )


@help_section_router.callback_query(F.data.startswith("faq_item_"))
async def faq_item_handler(callback: CallbackQuery):
    """Детальный ответ на вопрос FAQ"""
    await safe_answer_callback(callback)

    try:
        item_index = int(callback.data.replace("faq_item_", ""))
        faq_item = help_service.get_faq_item(item_index)

        if faq_item:
            text = f"❓ <b>{faq_item.question}</b>\n\n{faq_item.answer}"

            await callback.message.edit_text(
                text=text, reply_markup=faq_detail_keyboard(), parse_mode="HTML"
            )
        else:
            await callback.message.edit_text(
                text=Localization.help_error_not_found,
                reply_markup=faq_detail_keyboard(),
                parse_mode="HTML",
            )
    except (ValueError, IndexError):
        await callback.message.edit_text(
            text=Localization.help_error_not_found,
            reply_markup=faq_detail_keyboard(),
            parse_mode="HTML",
        )


@help_section_router.callback_query(F.data == "faq_back")
async def faq_back_handler(callback: CallbackQuery):
    """Возврат к списку FAQ"""
    await safe_answer_callback(callback)

    faq_items = help_service.get_faq_items()

    await callback.message.edit_text(
        text=Localization.help_faq_intro,
        reply_markup=faq_keyboard(faq_items),
        parse_mode="HTML",
    )


@help_section_router.callback_query(F.data == f"help_{HelpSection.instructions}")
async def instructions_handler(callback: CallbackQuery):
    """Инструкции по использованию бота"""
    await safe_answer_callback(callback)

    await callback.message.edit_text(
        text=Localization.help_instructions_text,
        reply_markup=help_main_keyboard(),
        parse_mode="HTML",
    )


@help_section_router.callback_query(F.data == f"help_{HelpSection.contact}")
async def contact_handler(callback: CallbackQuery):
    """Контактная информация"""
    await safe_answer_callback(callback)

    await callback.message.edit_text(
        text=Localization.help_contact_text,
        reply_markup=help_main_keyboard(),
        parse_mode="HTML",
    )
