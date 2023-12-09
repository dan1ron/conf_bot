import operator

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, KeyboardButton
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.kbd import (
    Start, Select, Button, Url, ListGroup
)
from aiogram_dialog.widgets.text import Const, Format

from config import ADMIN
from database import DB
from dialogs.states import Main, Admin, Subscribe, Tools
from magic_filter import F

# async def add_request(m: Message, button: Button, manager: DialogManager):
#     user = await DB.get_user(m.from_user.id)
#     if user.points <= 0:
#         await m.answer("У вас закончились поинты, приходите завтра")
#         return await manager.switch_to(Main.menu)
#     data = manager.current_context().dialog_data
#     request = Queue(**{
#         "id": m.from_user.id,
#         "ai": data['ai'],
#         "model": data['model'],
#         "image": data['image'] if 'image' in data else None,
#     })
#     await DB.add_requet(request)
#     user = await DB.get_user(m.from_user.id)
#     user.points -= 1
#     await DB.update_user(user)
#     await m.answer('Запрос отправлен')

async def menu_data(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id
    user = await DB.get_user(user_id)
    return {
        "is_admin": user.role == 'ADMIN',
    }

async def add_type(c: CallbackQuery, button: Select, manager: DialogManager, *args, **kwargs):
    manager.current_context().dialog_data['b_type'] = int(c.data.split(":")[1])
    await manager.switch_to(Main.sub_on_my_channel)



main_d = Dialog(
    Window(
        Format("🌟<b>Добро пожаловать на PRconf24 - главное событие этой зимы!</b> 👋\n"),
        Start(Const("Админ"), id="to_admin_b", state=Admin.menu, when="is_admin"),
        state=Main.menu,
        getter=menu_data,
        parse_mode="html",
    ),
    # Window(
    #     Format("🌟<b>Добро пожаловать на PRconf24 - главное событие этой зимы!</b> 👋\n"),
    #     Start(Const("Админ"), id="to_admin_b", state=Admin.menu, when="is_admin"),
    #     state=Main.menu,
    #     getter=menu_data,
    #     parse_mode="html",
    # ),
    launch_mode=LaunchMode.SINGLE_TOP

)
