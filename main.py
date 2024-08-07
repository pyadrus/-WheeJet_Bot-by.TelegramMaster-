import asyncio
import logging
import sys

from loguru import logger

from handlers.admin.admin_handlers import register_greeting_admin_handler
from handlers.user.check_out_the_warranty_handlers import register_check_out_the_warranty_handlers
from handlers.user.guarantee_chek_handlers import \
    register_guarantee_chek_handlers
from handlers.user.instructions_handlers import register_instructions_handlers
from handlers.user.user_handlers import register_greeting_user_handler
from system.dispatcher import dp, bot

logger.add("logs/log.log", retention="1 days", enqueue=True)  # Логирование бота


async def main() -> None:
    await dp.start_polling(bot)
    register_greeting_user_handler()  # Обработчик команды /start
    register_greeting_admin_handler()  # Обработчик команды /admin_start
    register_instructions_handlers()  # Обработчик команды /instructions
    register_check_out_the_warranty_handlers()  # Обработчик команды /check_out_the_warranty
    register_guarantee_chek_handlers()  # Обработчик команды /i_accept_the_terms_fill_out_the_form


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
