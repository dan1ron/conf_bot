from aiogram.dispatcher.filters.state import StatesGroup, State


class Main(StatesGroup):
    short_info = State()
    sub_on_my_channel = State()
    role = State()
    menu = State()


class Admin(StatesGroup):
    menu = State()
    msg_for_sending = State()
    confirm_sending = State()
    confirm_setting = State()
    stats = State()
    settings1 = State()
    settings2 = State()
    add_category = State()
    add_link = State()


class Subscribe(StatesGroup):
    main = State()
    tarif_1 = State()


class Tools(StatesGroup):
    type = State()
    bank = State()
