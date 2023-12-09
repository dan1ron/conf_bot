from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from database import DB


class CheckUserMiddleware(BaseMiddleware):
    async def check_availability_user(self, user_id: int, username):
        if not await DB.get_user(user_id):
            await DB.add_user(user_id, username)

    async def on_process_message(self, m: Message, data: dict):
        await self.check_availability_user(m.from_user.id, m.from_user.username)

    async def on_process_callback_query(self, c: CallbackQuery, data: dict):
        await self.check_availability_user(c.from_user.id, c.from_user.username)
