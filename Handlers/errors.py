from aiogram import types, Router
from aiogram.exceptions import TelegramAPIError

from createbot import logger


error_router = Router()


@error_router.errors()
async def error_handler(update: types.Update, exception: Exception):
    logger.error(f"Ошибка при обработке {update}: {exception}", exc_info=True)

    if isinstance(exception, TelegramAPIError):
        return True