from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from loguru import logger

from keyboards.keyboards import check_the_warranty_card_keyboard
from system.dispatcher import ADMIN_USER_ID
from system.dispatcher import bot, dp, router
from system.working_with_files import load_bot_info, save_bot_info


@router.callback_query(F.data == "check_the_warranty_card")
async def check_the_warranty_card_handlers(callback_query: types.CallbackQuery) -> None:
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.username
    user_first_name = callback_query.from_user.first_name
    user_last_name = callback_query.from_user.last_name
    logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name}")
    await bot.send_message(callback_query.from_user.id,
                           load_bot_info(messages="messages/check_the_warranty_card_messages.json"),
                           reply_markup=check_the_warranty_card_keyboard(),
                           disable_web_page_preview=True,
                           parse_mode="HTML"
                           )


class Formedit_check_the_warranty_card(StatesGroup):
    text_edit_check_the_warranty_card = State()


@router.message(Command("edit_check_the_warranty_card"))
async def edit_check_the_warranty_card(message: Message, state: FSMContext):
    """Обработчик команды /edit_check_the_warranty_card (только для админа)"""
    if message.from_user.id not in ADMIN_USER_ID:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return
    await message.answer("Введите новый текст, используя разметку HTML.")
    await state.set_state(Formedit_check_the_warranty_card.text_edit_check_the_warranty_card)


@router.message(Formedit_check_the_warranty_card.text_edit_check_the_warranty_card)
async def update_info(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений (для админа, чтобы обновить информацию)"""
    text = message.html_text
    bot_info = text
    save_bot_info(bot_info, file_path="messages/check_the_warranty_card_messages.json")  # Сохраняем информацию в JSON
    await message.reply("Информация обновлена.")
    await state.clear()


def register_check_the_warranty_card_handlers():
    """Регистрация обработчиков для бота"""
    dp.message.register(check_the_warranty_card_handlers)
    dp.message.register(edit_check_the_warranty_card)
