from aiogram import types, F
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from loguru import logger

from database.database import recording_user_data_of_the_launched_bot
from keyboards.keyboards import greeting_keyboard
from system.dispatcher import ADMIN_USER_ID
from system.dispatcher import bot, dp
from system.dispatcher import router
from system.working_with_files import load_bot_info
from system.working_with_files import save_bot_info


@dp.message(CommandStart())
async def user_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    if message.from_user.last_name is None:
        user_last_name = ''
    user_date = message.date.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name} {user_date}")
    recording_user_data_of_the_launched_bot(user_id, user_name, user_first_name, user_last_name, user_date)
    await bot.send_message(message.from_user.id,
                           load_bot_info(messages="messages/main_menu_messages.json"),
                           reply_markup=greeting_keyboard(),
                           parse_mode="HTML"
                           )


@router.callback_query(F.data == "back_to_menu")
async def instructions_handlers(callback_query: types.CallbackQuery) -> None:
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.username
    user_first_name = callback_query.from_user.first_name
    user_last_name = callback_query.from_user.last_name
    logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name}")
    await bot.send_message(callback_query.from_user.id,
                           load_bot_info(messages="messages/main_menu_messages.json"),
                           reply_markup=greeting_keyboard(),
                           parse_mode="HTML"
                           )


class FormeditMainMenu(StatesGroup):
    text_edit_main_menu = State()


@router.message(Command("edit_main_menu"))
async def edit_main_menu(message: Message, state: FSMContext):
    """Обработчик команды /edit_main_menu (только для админа)"""
    if message.from_user.id not in ADMIN_USER_ID:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return
    await message.answer("Введите новый текст, используя разметку HTML.")
    await state.set_state(FormeditMainMenu.text_edit_main_menu)


@router.message(FormeditMainMenu.text_edit_main_menu)
async def update_info(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений (для админа, чтобы обновить информацию)"""
    text = message.html_text
    bot_info = text
    save_bot_info(bot_info, file_path='messages/main_menu_messages.json')  # Сохраняем информацию в JSON
    await message.reply("Информация обновлена.")
    await state.clear()


def register_greeting_user_handler():
    """Регистрация обработчиков для бота"""
    dp.message.register(user_start_handler)
    dp.message.register(instructions_handlers)  # обработчик для кнопки "Назад"
    dp.message.register(edit_main_menu)  # обработчик для кнопки "Назад"

