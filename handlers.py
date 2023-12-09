from time import time

from aiogram import types
from aiogram_broadcaster import TextBroadcaster
from aiogram_dialog import StartMode, DialogManager

from config import ADMIN
from database.models import User
from dialogs.states import Admin, Main


async def start(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=Main.menu, mode=StartMode.RESET_STACK)


async def adm_handler(message: types.Message, dialog_manager: DialogManager):
    if message.from_user.id == ADMIN:
        await dialog_manager.start(state=Admin.menu, mode=StartMode.RESET_STACK)


async def errors_handler(u: types.Update, e: Exception):
    await TextBroadcaster(
        chats=ADMIN, text=f"Произошла ошибка: {e.__class__.__name__}({e})"
    ).run()
