import asyncio
import logging
import sys

from loguru import logger

from handlers.admin.admin_handlers import register_greeting_admin_handler
from handlers.user.check_out_the_warranty_handlers import register_check_out_the_warranty_handlers
from handlers.user.check_the_warranty_card_handlers import register_check_the_warranty_card_handlers
from handlers.user.download_warranty_card_handlers import register_download_warranty_card_handlers
from handlers.user.guarantee_chek_handlers import register_guarantee_chek_handlers
from handlers.user.instructions_handlers import register_instructions_handlers
from handlers.user.payment_handlers.payment_handlers import register_payment_handlers
from handlers.user.payment_handlers.payment_handlers_3_years import register_payment_handlers_3_years
from handlers.user.user_handlers import register_greeting_user_handler
from system.dispatcher import dp, bot

logger.add("logs/log.log", retention="1 days", enqueue=True)  # Логирование бота


async def main() -> None:
    await dp.start_polling(bot)
    register_payment_handlers_3_years() # Оплата гарантийника 3 года
    register_greeting_user_handler()  # Обработчик команды /start
    register_greeting_admin_handler()  # Обработчик команды /admin_start
    register_instructions_handlers()  # Обработчик команды /instructions
    register_check_out_the_warranty_handlers()  # Обработчик команды /check_out_the_warranty
    register_guarantee_chek_handlers()  # Обработчик команды /i_accept_the_terms_fill_out_the_form
    register_check_the_warranty_card_handlers()  # Обработчик команды /check_the_warranty_card
    register_download_warranty_card_handlers()
    register_payment_handlers() # Оплата гарантийного талона на 2 - 3 года



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
