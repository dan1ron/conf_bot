from aiogram.types import (
    Message,
    CallbackQuery,
    ContentType,
)
from aiogram_broadcaster import MessageBroadcaster
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    SwitchTo,
    Button,
    Row,
)
from aiogram_dialog.widgets.text import Const, Format, Multi

from database import DB
from dialogs.states import Admin, Main


async def stats_data(dialog_manager: DialogManager, **kwargs):
    all_users_count = await DB.users_count()
    return {
        "all_users": all_users_count,
    }


async def to_menu(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(Main.menu, mode=StartMode.RESET_STACK)
    await c.answer()


async def get_setting(dialog_manager: DialogManager, **kwargs):
    return {"value": dialog_manager.current_context().dialog_data.get("setting")}


async def sending_msg_handler(m: Message, dialog: Dialog, manager: DialogManager):
    manager.current_context().dialog_data["msg"] = dict(m)
    await manager.dialog().switch_to(Admin.confirm_sending)


async def start_sending(c: CallbackQuery, button: Button, manager: DialogManager):
    data = manager.current_context().dialog_data
    users = [i.id for i in await DB.get_users()]
    msg = Message.to_object(data.get("msg"))
    if users:
        await MessageBroadcaster(chats=list(users), message=msg).run()
    await c.answer()


admin_d = Dialog(
    Window(
        Const("Меню"),
        SwitchTo(
            Const("Рассылка"),
            id="sending_b",
            state=Admin.msg_for_sending,
        ),
        SwitchTo(Const("Статистика"), id="stat_b", state=Admin.stats),
        state=Admin.menu,
    ),
    Window(
        Const("Напишите сообщение которое хотите отправить"),
        MessageInput(sending_msg_handler, content_types=[ContentType.ANY]),
        SwitchTo(Const("Назад"), id="back_b", state=Admin.menu),
        state=Admin.msg_for_sending,
    ),
    Window(
        Const("Вы уверены что хотите отправить рассылку"),
        Row(
            SwitchTo(Const("Да"), id="yes_b", state=Admin.sending_completed, on_click=start_sending),
            SwitchTo(Const("Нет"), id="no_b", state=Admin.msg_for_sending),
        ),
        state=Admin.confirm_sending,
    ),
    Window(
        Const("Сообщение отправлено"),
        SwitchTo(Const("В меню"), id="back_b", state=Admin.menu),
        state=Admin.sending_completed,
    ),
    Window(
        Multi(
            Format("Всего пользователей: {all_users}\n"),
        ),
        SwitchTo(Const("Назад"), id="back_b", state=Admin.menu),
        state=Admin.stats,
        getter=stats_data,
    ),
)
