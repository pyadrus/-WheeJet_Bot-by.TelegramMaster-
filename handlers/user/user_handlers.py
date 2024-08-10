from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger
from peewee import *
from keyboards.keyboards import greeting_keyboard
from system.dispatcher import bot, dp
from system.dispatcher import router
from system.working_with_files import load_bot_info

# Создайте модель для таблицы в базе данных
db = SqliteDatabase('my_database.db')


class UserStart(Model):
    telegram_id = CharField()  # Идентификатор пользователя Telegram
    telegram_username = CharField()  # Идентификатор пользователя Telegram (username)
    user_first_name = CharField()  # Артикул товара
    user_last_name = CharField()  # Номер заказа
    user_date = CharField()  # Артикул товара

    class Meta:
        database = db


@dp.message(CommandStart())
async def user_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_date = message.date.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name} {user_date}")

    db.create_tables([UserStart])
    user_start = UserStart.create(
        telegram_id=user_id,
        telegram_username=user_name,
        user_first_name=user_first_name,
        user_last_name=user_last_name,
        user_date=user_date,
    )
    user_start.save()

    await bot.send_message(message.from_user.id,
                           load_bot_info(messages="media/messages/main_menu_messages.json"),
                           reply_markup=greeting_keyboard(),
                           disable_web_page_preview=True, )


@router.callback_query(F.data == "back_to_menu")
async def instructions_handlers(callback_query: types.CallbackQuery) -> None:
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.username
    user_first_name = callback_query.from_user.first_name
    user_last_name = callback_query.from_user.last_name
    logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name}")
    await bot.send_message(callback_query.from_user.id,
                           load_bot_info(messages="media/messages/main_menu_messages.json"),
                           reply_markup=greeting_keyboard(),
                           disable_web_page_preview=True, )


def register_greeting_user_handler():
    """Регистрация обработчиков для бота"""
    dp.message.register(user_start_handler)
    dp.message.register(instructions_handlers)  # обработчик для кнопки "Назад"
