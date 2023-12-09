import operator

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
    Select,
    Start
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


async def get_categories(dialog_manager: DialogManager, **kwargs):
    return {
        "categories": await DB.get_categories()
    }


async def get_links(dialog_manager: DialogManager, **kwargs):
    category = dialog_manager.current_context().dialog_data.get('category')
    return {
        "links": await DB.get_links(category)
    }


def add_type(type):
    async def add_model(c: CallbackQuery, button: Select, manager: DialogManager, *args, **kwargs):
        manager.current_context().dialog_data['adding_model'] = dict(type=type, data=c.data)
        await manager.switch_to(Main.sub_on_my_channel)

    return add_model


def del_type(type):
    async def del_model(c: CallbackQuery, button: Select, manager: DialogManager, *args, **kwargs):
        manager.current_context().dialog_data['del_type'] = dict(type=type, data=c.data)
        await manager.switch_to(Admin.confirm_setting)

    return del_model

async def get_setting(dialog_manager: DialogManager, **kwargs):
    return {"value": dialog_manager.current_context().dialog_data.get("setting")}


async def sending_msg_handler(m: Message, dialog: Dialog, manager: DialogManager):
    manager.current_context().dialog_data["msg"] = dict(m)
    await manager.dialog().switch_to(Admin.confirm_setting)


async def save_setting(c: CallbackQuery, dialog: Dialog, manager: DialogManager):
    setting = manager.current_context().dialog_data.get("setting")
    value_setting = manager.current_context().dialog_data.get("value_setting")
    # TODO: сделать сохранение настроек
    # await manager.dialog().switch_to(Admin.edit_settings)


async def start_sending(c: CallbackQuery, button: Button, manager: DialogManager):
    data = manager.current_context().dialog_data
    users = [i.id for i in await DB.get_users()]
    msg = Message.to_object(data.get("msg"))
    if users:
        await MessageBroadcaster(chats=list(users), message=msg).run()
    await c.answer()

async def delete_setting(c: CallbackQuery, button: Button, manager: DialogManager):
    model = manager.current_context().dialog_data.get('del_type')
    model_type = model.get('type')
    model_data = model.get('data')
    await dict(category=DB.del_link, link=DB.del_category).get(model_type)(model_data)
    # await manager.dialog().switch_to(Admin.) if model_type



admin_d = Dialog(
    Window(
        Const("Меню"),
        SwitchTo(
            Const("Рассылка"),
            id="sending_b",
            state=Admin.msg_for_sending,
        ),
        SwitchTo(Const("Настройки"), id="settings_b", state=Admin.settings1),
        SwitchTo(Const("Статистика"), id="stat_b", state=Admin.stats),
        Button(Const("В меню"), id="to_menu_b", on_click=to_menu),
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
            SwitchTo(Const("Да"), id="yes_b", state=Admin.menu, on_click=start_sending),
            SwitchTo(Const("Нет"), id="no_b", state=Admin.msg_for_sending),
        ),
        state=Admin.confirm_sending,
    ),
    Window(
        Multi(
            Format("Всего пользователей: {all_users}\n"),
        ),
        SwitchTo(Const("Назад"), id="back_b", state=Admin.menu),
        state=Admin.stats,
        getter=stats_data,
    ),
    Window(
        Const("Категории"),
        Select(
            Format("{item.name}"),
            id="c_type",
            items="categories",
            on_click=add_type,
            item_id_getter=operator.itemgetter(1)
        ),
        Start(Const("Добавить"), id="to_add_category", state=Admin.menu),
        SwitchTo(Const("Назад"), id="back_to_AM", state=Admin.menu),
        state=Admin.settings1,
        getter=get_categories
    ),
    Window(
        Format("{category}"),
        Select(
            Format("{item.name} - Удалить"),
            id="c_type",
            items="links",
            on_click=del_type('link'),
            item_id_getter=operator.itemgetter(1)
        ),
        SwitchTo(Format("Удалить категорию"), id='del_category', state=Admin.confirm_setting,
                 on_click=del_type('category')),
        Start(Const("Добавить ссылку"), id="to_add_category", state=Admin.menu),
        SwitchTo(Const("Назад"), id="back_to_AM", state=Admin.settings1),
        state=Admin.settings2,
        getter=get_links,
    ),
    Window(
        Format("Введите название категории"),
        Row(
            MessageInput(sending_msg_handler),
            SwitchTo(Const("Назад"), id="back_to_AS", state=Admin.settings1),
        ),
        state=Admin.add_category,
        getter=get_setting
    ),
    Window(
        Format("Введите ссылку в формате: Сбербанк:https://url.com"),
        Row(
            MessageInput(sending_msg_handler),
            SwitchTo(Const("Назад"), id="back_to_AS", state=Admin.settings2),
        ),
        state=Admin.add_link,
        getter=get_setting
    ),
    Window(
        Const("Вы уверены, что хотите удалить?"),
        Row(
            SwitchTo(Const("Да"), id="yes_b", state=Admin.menu, on_click=start_sending),
            SwitchTo(Const("Нет"), id="no_b", state=Admin.settings1),
        ),
        state=Admin.confirm_setting,
    ),

)
