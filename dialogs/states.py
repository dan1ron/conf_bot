from aiogram.dispatcher.filters.state import StatesGroup, State


class Main(StatesGroup):
    role = State()
    menu = State()
    schedule = State()


class Admin(StatesGroup):
    menu = State()
    msg_for_sending = State()
    confirm_sending = State()
    sending_completed = State()
    stats = State()
    clear_cache = State()


class Subscribe(StatesGroup):
    main = State()
    tarif_1 = State()


class Tools(StatesGroup):
    type = State()
    bank = State()
