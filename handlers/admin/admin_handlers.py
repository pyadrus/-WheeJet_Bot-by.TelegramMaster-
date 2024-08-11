import os

import openpyxl
from aiogram import F
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.types import Message
from loguru import logger

from database.database import UserStart
from keyboards.admin_keyboards import admin_keyboard
from system.dispatcher import bot, ADMIN_USER_ID
from system.dispatcher import dp
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
                                                             "✔️ /edit_instructions - текст меню 'инструкция'\n"

                                                             "<b>Получение данных:</b>\n"
                                                             "✔️ /get_users_who_launched_the_bot - Получение данных пользователей, запускающих бота\n\n"

                                                             "/start - начальное меню\n", parse_mode="HTML")


def create_excel_file_start(orders):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    # Заголовки столбцов
    sheet['A1'] = 'ID аккаунта пользователя'
    sheet['B1'] = 'username'
    sheet['C1'] = 'Имя'
    sheet['D1'] = 'Фамилия'
    sheet['E1'] = 'Дата запуска бота'
    # Заполнение данными заказов
    for index, order in enumerate(orders, start=2):
        sheet.cell(row=index, column=1).value = order[0]  # ID аккаунта пользователя
        sheet.cell(row=index, column=2).value = order[1]  # username
        sheet.cell(row=index, column=3).value = order[2]  # Имя
        sheet.cell(row=index, column=4).value = order[3]  # Фамилия
        sheet.cell(row=index, column=5).value = order[4]  # Дата запуска бота

    return workbook  # Возвращаем объект workbook


# Функция для чтения данных из базы данных
def reading_from_database():
    # Извлекаем все записи из таблицы UserStart
    query = UserStart.select()

    # Формируем список из кортежей с данными для передачи в create_excel_file_start
    orders = [
        (user.telegram_id, user.telegram_username, user.user_first_name, user.user_last_name, user.user_date)
        for user in query
    ]

    return orders


@router.message(Command("get_users_who_launched_the_bot"))
async def get_users_who_launched_the_bot(message: types.Message, state: FSMContext):
    """Получение данных пользователей, запускающих бота"""
    await state.clear()  # Завершаем текущее состояние машины состояний
    try:
        if message.from_user.id not in [535185511, 301634256]:
            await message.reply('У вас нет доступа к этой команде.')
            return
        orders = reading_from_database()
        workbook = create_excel_file_start(orders)  # Создание файла Excel
        filename = 'Данные пользователей запустивших бота.xlsx'
        workbook.save(filename)  # Сохранение файла
        file = FSInputFile(filename)
        text = ("Данные пользователей зарегистрированных в боте\n\n"
                "Для возврата в начальное меню нажми на /start или /help")
        await bot.send_document(message.from_user.id, document=file, caption=text)  # Отправка файла пользователю
        os.remove(filename)  # Удаление файла
    except Exception as e:
        logger.error(e)


def register_greeting_admin_handler():
    """Регистрация обработчиков для бота"""
    dp.message.register(admin_start_handler)
    dp.message.register(admin_send_start)
