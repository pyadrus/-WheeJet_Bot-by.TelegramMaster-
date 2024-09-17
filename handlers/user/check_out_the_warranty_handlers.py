from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from loguru import logger

from keyboards.keyboards import check_out_the_warranty_keyboard
from system.dispatcher import ADMIN_USER_ID
from system.dispatcher import bot, dp, router
from system.working_with_files import load_bot_info
from system.working_with_files import save_bot_info


@router.callback_query(F.data == "check_out_the_warranty")
async def check_out_the_warranty_handlers(callback_query: types.CallbackQuery) -> None:
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.username
    user_first_name = callback_query.from_user.first_name
    user_last_name = callback_query.from_user.last_name
    logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name}")

    await bot.send_message(callback_query.from_user.id,
                           load_bot_info(messages="messages/check_out_the_warranty_messages.json"),
                           reply_markup=check_out_the_warranty_keyboard(),
                           disable_web_page_preview=True)


class FormeditCheckOutTheWarranty(StatesGroup):
    text_edit_check_out_the_warranty = State()


@router.message(Command("edit_check_out_the_warranty"))
async def edit_instructions(message: Message, state: FSMContext):
    """Обработчик команды /edit_main_menu (только для админа)"""
    if message.from_user.id not in ADMIN_USER_ID:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return
    await message.answer("Введите новый текст, используя разметку HTML.")
    await state.set_state(FormeditCheckOutTheWarranty.text_edit_check_out_the_warranty)


@router.message(FormeditCheckOutTheWarranty.text_edit_check_out_the_warranty)
async def update_info(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений (для админа, чтобы обновить информацию)"""
    text = message.html_text
    bot_info = text
    save_bot_info(bot_info, file_path="messages/check_out_the_warranty_messages.json")  # Сохраняем информацию в JSON
    await message.reply("Информация обновлена.")
    await state.clear()


def register_check_out_the_warranty_handlers():
    """Регистрация обработчиков для бота"""
    dp.message.register(check_out_the_warranty_handlers)
    dp.message.register(edit_instructions)
