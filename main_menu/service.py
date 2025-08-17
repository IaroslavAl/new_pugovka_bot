from asyncio import Lock
from aiogram import types
from bot_instance import get_bot


class MenuService:
    def __init__(self):
        self.user_menus: dict[int, int] = {}
        self.user_locks: dict[int, Lock] = {}

    @property
    def bot(self):
        return get_bot()

    async def get_lock(self, chat_id: int) -> Lock:
        if chat_id not in self.user_locks:
            self.user_locks[chat_id] = Lock()
        return self.user_locks[chat_id]

    async def show_menu(
        self, chat_id: int, text: str, keyboard: types.InlineKeyboardMarkup
    ):
        lock = await self.get_lock(chat_id)
        async with lock:
            old_id = self.user_menus.get(chat_id)
            if old_id:
                await self.bot.delete_message(chat_id, old_id)

            msg = await self.bot.send_message(
                chat_id, text, reply_markup=keyboard, parse_mode="HTML"
            )

            self.user_menus[chat_id] = msg.message_id
            return msg

    async def delete_menu(self, chat_id: int):
        lock = await self.get_lock(chat_id)
        async with lock:
            old_id = self.user_menus.get(chat_id)
            if old_id:
                await self.bot.delete_message(chat_id, old_id)
                self.user_menus.pop(chat_id, None)
