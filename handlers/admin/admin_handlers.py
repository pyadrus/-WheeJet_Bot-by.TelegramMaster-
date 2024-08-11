from aiogram import F
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from keyboards.admin_keyboards import admin_keyboard
from system.dispatcher import ADMIN_USER_ID
from system.dispatcher import bot, dp
from system.dispatcher import router


@dp.message(F.text == "/admin_start")
async def admin_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_date = message.date.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name} {user_date}")
    sign_up_text = "Добро пожаловать Admin"
    await bot.send_message(message.from_user.id, sign_up_text, reply_markup=admin_keyboard(),
                           disable_web_page_preview=True)


@router.callback_query(F.data == "admin_commands")
async def admin_send_start(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия 👋"""
    await state.clear()  # Завершаем текущее состояние машины состояний
    """Админ панель"""
    if callback_query.from_user.id not in ADMIN_USER_ID:
        await bot.send_message(callback_query.from_user.id, text="У вас нет прав на выполнение этой команды.")
        return
    await bot.send_message(callback_query.from_user.id, text="Команды админа:\n\n"

                                                             "<b>Редактирование текста и получение данных:</b>\n\n"

                                                             "<b>Редактирование текста:</b>\n"
                                                             "✔️ /edit_main_menu - текст меню бота\n"

                                                             "<b>Получение данных:</b>\n"
                                                             "✔️ /get_users_who_launched_the_bot - Получение данных пользователей, запускающих бота\n\n"

                                                             "/start - начальное меню\n", parse_mode="HTML")


def register_greeting_admin_handler():
    """Регистрация обработчиков для бота"""
    dp.message.register(admin_start_handler)
    dp.message.register(admin_send_start)
