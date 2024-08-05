import asyncio
import logging
import sys

from loguru import logger

from handlers.admin.admin_handlers import register_greeting_admin_handler
from handlers.user.user_handlers import register_greeting_user_handler
from system.dispatcher import dp, bot

logger.add("logs/log.log", retention="1 days", enqueue=True)  # Логирование бота


async def main() -> None:
    await dp.start_polling(bot)
    register_greeting_user_handler()  # Обработчик команды /start
    register_greeting_admin_handler()  # Обработчик команды /admin_start


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
