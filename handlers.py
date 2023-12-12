from time import time

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram_broadcaster import TextBroadcaster
from aiogram_dialog import StartMode, DialogManager

from config import ADMIN
from database import DB
from database.models import User
from dialogs.states import Admin, Main


async def start(message: types.Message, dialog_manager: DialogManager):
    await message.answer(
        '🌟<b>Добро пожаловать на PRconf24 - главное событие этой зимы!</b> 👋\n'
        'Наш бот - твой надежный гид! Он знает расписание вдоль и поперёк, '
        'напомнит о грядущих блоках и даст доступ к контактам организаторов. '
        'С ним ты всегда на шаге впереди! 📝😊',
        parse_mode='html',
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Расписание')]], resize_keyboard=True)
    )

async def schedule(message: types.Message, dialog_manager: DialogManager):
    await message.answer(
        "<b>Д‌ень #1</b>\n"
        "<b>17:00</b> – Начало регистрации\n" 
        "<b>18:30</b> – Открытие конференции\n"
        "<b>18:50</b> – Ледокол\n"
        "<b>19:00</b> – СЕССИЯ #1\n"
        "<b>20:30</b> – Распределение на ночлег + задание\n\n"
        "<b>День #2</b>\n"
        "<b>9:00</b> – COFFEE-BREAKE\n"
        "<b>9:30</b> – Приветствие, молитва\n"
        "<b>10:00</b> – проверка задания\n" 
        "<b>11:00</b> - COFFEE-BREAKE\n"
        "<b>11:20</b> - СЕМИНАРЫ\n"
        "<b>12:30</b> – Обед\n"
        "<b>13:30</b> – Общая игра\n"
        "<b>14:30</b> - COFFEE-BREAKE\n"
        "<b>15:00</b> - СЕССИЯ #3\n"
        "<b>16:30</b> – Общая фотография\n"
        "<b>17:00</b> - Закрытие конференции\n",
        parse_mode='html'
    )


async def adm_handler(message: types.Message, dialog_manager: DialogManager):
    if (await DB.get_user(message.from_user.id)).role == "ADMIN":
        await dialog_manager.start(state=Admin.menu, mode=StartMode.RESET_STACK)

async def clear_cache(message: types.Message, dialog_manager: DialogManager):
    if message.from_user.id == ADMIN:
        await dialog_manager.start(state=Admin.clear_cache, mode=StartMode.RESET_STACK)



async def errors_handler(u: types.Update, e: Exception):
    await TextBroadcaster(
        chats=ADMIN, text=f"Произошла ошибка: {e.__class__.__name__}({e})"
    ).run()