from time import time

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram_broadcaster import TextBroadcaster
from aiogram_dialog import StartMode, DialogManager

from config import ADMIN
from database.models import User
from dialogs.states import Admin, Main


async def start(message: types.Message, dialog_manager: DialogManager):
    await message.answer(
        '🌟<b>Добро пожаловать на PRconf24 - главное событие этой зимы!</b> 👋\n',
        parse_mode='html',
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Расписание')]], resize_keyboard=True)
    )

async def schedule(message: types.Message, dialog_manager: DialogManager):
    await message.answer(
        "<b>3 января</b>\n\n"
        "<b>18:00</b> – РЕГИСТРАЦИЯ + кофе, бутерброды\n" 
        "<b>18:30</b> – ПРИВЕТСТВИЕ\n"
        "<b>18:50</b> –ледокольчик\n"
        "СЕССИЯ No1 (Макс Чепель)\n"
        "<b>20:30</b> – РАСПРЕДЕЛЕНИЕ НА НОЧЛЕГ + ДОМАШКА\n\n"
        "<b>4 января</b>\n\n"
        "<b>9:00</b> – кофе, бутерброды\n"
        "<b>9:30</b> – приветствие, молитва\n"
        "<b>10:00</b> – проверка домашнего задания\n" 
        "<b>11:00</b> - COFFEE-BREAKE\n"
        "<b>11:20</b> - СЕССИЯ No2 - (?)\n"
        "<b>12:30</b> – ОБЕД\n"
        "<b>13:30</b> – квиз\n"
        "<b>14:30</b> - КОФЕ, ПЕЧЕНЬКИ\n"
        "<b>15:00</b> - СЕССИЯ No 3 (Паша Воложанин)\n"
        "<b>16:30</b> – УЖИН/ОБЩАЯ ФОТОГРАФИЯ\n"
        "<b>17:00</b> - РАЗЪЕЗД\n",
        parse_mode='html'
    )


async def adm_handler(message: types.Message, dialog_manager: DialogManager):
    if message.from_user.id == ADMIN:
        await dialog_manager.start(state=Admin.menu, mode=StartMode.RESET_STACK)


async def errors_handler(u: types.Update, e: Exception):
    await TextBroadcaster(
        chats=ADMIN, text=f"Произошла ошибка: {e.__class__.__name__}({e})"
    ).run()
