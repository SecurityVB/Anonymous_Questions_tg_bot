import sys
import asyncio

from DataBase.sqlite_db import sql_start
from Handlers.errors import error_router
from Handlers.payment import payment_router
from createbot import *
from Handlers.commands import commands_router
from Handlers.inlinekeyboard import inline_kb_router
from createbot import logger


async def on_startup():
    logger.info('Бот вышел в онлайн.')
    sql_start()
    dp.include_router(payment_router)
    dp.include_router(commands_router)
    dp.include_router(inline_kb_router)
    dp.include_router(error_router)
    await dp.start_polling(bot, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    asyncio.run(on_startup())

