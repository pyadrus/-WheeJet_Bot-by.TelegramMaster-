from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from loguru import logger

from keyboards.keyboards import instructions_keyboard
from system.dispatcher import ADMIN_USER_ID
from system.dispatcher import bot, dp, router
from system.working_with_files import load_bot_info, save_bot_info


@router.callback_query(F.data == "instructions")
async def instructions_handlers(callback_query: types.CallbackQuery) -> None:
    try:
        user_id = callback_query.from_user.id

        user_name = callback_query.from_user.username
        if callback_query.from_user.username is None:
            user_name = ''  # Установим пустую строку вместо None

        user_first_name = callback_query.from_user.first_name
        user_last_name = callback_query.from_user.last_name
        logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name}")
        await bot.send_message(callback_query.from_user.id,
                               load_bot_info(messages="messages/instructions_messages.json"),
                               reply_markup=instructions_keyboard(),
                               disable_web_page_preview=True,
                               parse_mode="HTML"
                               )
    except Exception as e:
        logger.error(f"Ошибка: {e}")


class FormeditInstructions(StatesGroup):
    text_edit_instructions = State()


@router.message(Command("edit_instructions"))
async def edit_instructions(message: Message, state: FSMContext):
    """Обработчик команды /edit_main_menu (только для админа)"""
    try:
        if message.from_user.id not in ADMIN_USER_ID:
            await message.reply("У вас нет прав на выполнение этой команды.")
            return
        await message.answer("Введите новый текст, используя разметку HTML.")
        await state.set_state(FormeditInstructions.text_edit_instructions)
    except Exception as e:
        logger.error(f"Ошибка: {e}")


@router.message(FormeditInstructions.text_edit_instructions)
async def update_info(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений (для админа, чтобы обновить информацию)"""
    try:
        text = message.html_text
        bot_info = text
        save_bot_info(bot_info, file_path="messages/instructions_messages.json")  # Сохраняем информацию в JSON
        await message.reply("Информация обновлена.")
        await state.clear()
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def register_instructions_handlers():
    """Регистрация обработчиков для бота"""
    dp.message.register(instructions_handlers)
    dp.message.register(edit_instructions)
