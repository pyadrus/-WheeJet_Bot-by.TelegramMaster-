from aiogram import types, F
from loguru import logger

from keyboards.keyboards import instructions_keyboard
from system.dispatcher import bot, dp, router


@router.callback_query(F.data == "instructions")
async def instructions_handlers(callback_query: types.CallbackQuery) -> None:
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.username
    user_first_name = callback_query.from_user.first_name
    user_last_name = callback_query.from_user.last_name
    logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name}")
    sign_up_text = "Вы можете ознакомиться с инструкцией по ссылке ниже"
    await bot.send_message(callback_query.from_user.id, sign_up_text, reply_markup=instructions_keyboard(),
                           disable_web_page_preview=True)


def register_instructions_handlers():
    """Регистрация обработчиков для бота"""
    dp.message.register(instructions_handlers)
