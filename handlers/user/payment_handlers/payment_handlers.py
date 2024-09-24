
from aiogram import types, F
from loguru import logger

from keyboards.keyboards import extended_warranty_2_years_continue_keyboard, extended_warranty_3_years_continue_keyboard
from system.dispatcher import bot, dp, router
from system.working_with_files import load_bot_info


@router.callback_query(F.data == "extended_warranty_2_years")
async def extended_warranty_2_years_handlers(callback_query: types.CallbackQuery) -> None:
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.username
    user_first_name = callback_query.from_user.first_name
    user_last_name = callback_query.from_user.last_name
    logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name}")
    await bot.send_message(callback_query.from_user.id,
                           load_bot_info(messages="messages/extended_warranty.json"),
                           reply_markup=extended_warranty_2_years_continue_keyboard(),
                           disable_web_page_preview=True,
                           parse_mode="HTML"
                           )

@router.callback_query(F.data == "extended_warranty_3_years")
async def extended_warranty_3_years_handlers(callback_query: types.CallbackQuery) -> None:
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.username
    user_first_name = callback_query.from_user.first_name
    user_last_name = callback_query.from_user.last_name
    logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name}")
    await bot.send_message(callback_query.from_user.id,
                           load_bot_info(messages="messages/extended_warranty.json"),
                           reply_markup=extended_warranty_3_years_continue_keyboard(),
                           disable_web_page_preview=True,
                           parse_mode="HTML"
                           )

def register_payment_handlers():
    """Регистрация обработчиков для бота"""
    dp.message.register(extended_warranty_2_years_handlers)
    dp.message.register(extended_warranty_3_years_handlers)
