import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_dialog import DialogRegistry
from config import ADMIN, token
from dialogs.admin import admin_d
from dialogs.main import main_d
from handlers import start, adm_handler, errors_handler
# from dialogs.main import main_d
from middlewares import CheckUserMiddleware

logging.basicConfig(level=logging.INFO)




async def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("match-bot").setLevel(logging.DEBUG)
    storage = MemoryStorage()
    # storage = RedisStorage2()
    bot = Bot(token=token)
    dp = Dispatcher(bot, storage=storage)

    dp.setup_middleware(CheckUserMiddleware())
    dp.register_message_handler(start, text="/start", state="*")
    dp.register_message_handler(adm_handler, text="/adm", state="*")
    dp.register_errors_handler(errors_handler, exception=Exception)

    registry = DialogRegistry(dp)
    registry.register(main_d)
    registry.register(admin_d)
    # registry.register(main_d)


    await dp.start_polling()

    logging.warning("Shutting down..")
    await dp.bot.session.close()
    await dp.bot.session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bye!")


if __name__ == "__main__":
    asyncio.run(main())
