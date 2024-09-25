import json
import sqlite3

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from loguru import logger
from yookassa import Configuration, Payment

from keyboards.payment_keyboards import extended_warranty_2_years_continue_keyboard, \
    extended_warranty_3_years_continue_keyboard
from system.dispatcher import bot, dp, router, SECRET_KEY, ACCOUNT_ID, ADMIN_CHAT_ID
from system.working_with_files import load_bot_info


@router.callback_query(F.data == "extended_warranty_2_years")
async def extended_warranty_2_years_handlers(callback_query: types.CallbackQuery) -> None:
    logger.info(f"{callback_query.from_user.id} {callback_query.from_user.username} "
                f"{callback_query.from_user.first_name} {callback_query.from_user.last_name}")

    url, payment = payment_yookassa_program_setup_service()

    await bot.send_message(callback_query.from_user.id,
                           load_bot_info(messages="messages/extended_warranty.json"),
                           reply_markup=extended_warranty_2_years_continue_keyboard(url, payment),
                           disable_web_page_preview=True,
                           parse_mode="HTML"
                           )


@dp.callback_query(F.data.startswith("check_service"))
async def check_payment_program_setup_service(callback_query: types.CallbackQuery, state: FSMContext):
    split_data = callback_query.data.split("_")
    logger.info(split_data[2])
    # Check the payment status using the YooKassa API
    payment_info = Payment.find_one(split_data[2])
    logger.info(payment_info)
    product = "Расширенная гарантия 2 года"
    if payment_info.status == "succeeded":  # Process the payment status
        payment_status = "succeeded"
        date = payment_info.captured_at
        logger.info(date)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users_pay (user_id, first_name, last_name, username,
                                                                payment_info, product, date, payment_status)''')
        cursor.execute('''INSERT INTO users_pay (user_id, first_name, last_name, username, payment_info, 
                                                      product, date, payment_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (callback_query.from_user.id,
                        callback_query.from_user.first_name,
                        callback_query.from_user.last_name,
                        callback_query.from_user.username, payment_info.id, product, date, payment_status))
        conn.commit()

        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Пользователь:\n"
                                                           f"ID {callback_query.from_user.id},\n"
                                                           f"Username: @{callback_query.from_user.username},\n"
                                                           f"Имя: {callback_query.from_user.first_name},\n"
                                                           f"Фамилия: {callback_query.from_user.last_name},\n\n"
                                                           f"Приобрел 'Дополнительную гарантию на 2 года'")

        await bot.send_message(callback_query.from_user.id,
                               "Оплата прошла успешно‼️ \n"
                               "Для возврата в начальное меню, нажмите: /start")
    else:
        await bot.send_message(callback_query.message.chat.id, "Payment failed.")

def payment_yookassa_program_setup_service():
    """
    Оплата ЮKassa
    карта для тестирования оплаты (2202 4743 0132 2987)
    https://yookassa.ru/developers/payment-acceptance/testing-and-going-live/testing?lang=ru#test-bank-card
    """
    logger.info(f"ACCOUNT_ID: {ACCOUNT_ID}, SECRET_KEY {SECRET_KEY}")
    Configuration.account_id = ACCOUNT_ID
    Configuration.secret_key = SECRET_KEY

    payment = Payment.create(
        {"amount": {"value": 1300.00, "currency": "RUB"}, "capture": True,
         "confirmation": {"type": "redirect", "return_url": "https://t.me/teeest_paaay_bot"},
         "description": "Расширенная гарантия 2 года",
         "metadata": {'order_number': '1'},
         "receipt": {"customer": {"email": "zh.vitaliy92@yandex.ru"},
                     "items": [
                         {
                             "description": "Расширенная гарантия 2 года ",  # Название товара
                             "quantity": "1",
                             "amount": {"value": 1300.00, "currency": "RUB"},  # Сумма и валюта
                             "vat_code": "1"}]}})

    payment_data = json.loads(payment.json())
    payment_id = payment_data['id']
    payment_url = (payment_data['confirmation'])['confirmation_url']
    logger.info(f"Ссылка для оплаты: {payment_url}, ID оплаты {payment_id}")
    return payment_url, payment_id


@router.callback_query(F.data == "extended_warranty_3_years")
async def extended_warranty_3_years_handlers(callback_query: types.CallbackQuery) -> None:
    logger.info(f"{callback_query.from_user.id} {callback_query.from_user.username} "
                f"{callback_query.from_user.first_name} {callback_query.from_user.last_name}")

    url, payment = payment_yookassa_program_setup_service_3()

    await bot.send_message(callback_query.from_user.id,
                           load_bot_info(messages="messages/extended_warranty.json"),
                           reply_markup=extended_warranty_3_years_continue_keyboard(url, payment),
                           disable_web_page_preview=True,
                           parse_mode="HTML"
                           )


@dp.callback_query(F.data.startswith("check_service3"))
async def check_payment_program_setup_service_3(callback_query: types.CallbackQuery, state: FSMContext):
    split_data = callback_query.data.split("_")
    logger.info(split_data[2])
    # Check the payment status using the YooKassa API
    payment_info = Payment.find_one(split_data[2])
    logger.info(payment_info)
    product = "Расширенная гарантия 3 года"
    if payment_info.status == "succeeded":  # Process the payment status
        payment_status = "succeeded"
        date = payment_info.captured_at
        logger.info(date)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users_pay (user_id, first_name, last_name, username,
                                                                payment_info, product, date, payment_status)''')
        cursor.execute('''INSERT INTO users_pay (user_id, first_name, last_name, username, payment_info, 
                                                      product, date, payment_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (callback_query.from_user.id,
                        callback_query.from_user.first_name,
                        callback_query.from_user.last_name,
                        callback_query.from_user.username, payment_info.id, product, date, payment_status))
        conn.commit()

        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Пользователь:\n"
                                                           f"ID {callback_query.from_user.id},\n"
                                                           f"Username: @{callback_query.from_user.username},\n"
                                                           f"Имя: {callback_query.from_user.first_name},\n"
                                                           f"Фамилия: {callback_query.from_user.last_name},\n\n"
                                                           f"Приобрел 'Дополнительную гарантию на 3 года'")

        await bot.send_message(callback_query.from_user.id,
                               "Оплата прошла успешно‼️ \n"
                               "Для возврата в начальное меню, нажмите: /start")
    else:
        await bot.send_message(callback_query.message.chat.id, "Payment failed.")


def payment_yookassa_program_setup_service_3():
    """
    Оплата ЮKassa
    карта для тестирования оплаты (2202 4743 0132 2987)
    https://yookassa.ru/developers/payment-acceptance/testing-and-going-live/testing?lang=ru#test-bank-card
    """
    logger.info(f"ACCOUNT_ID: {ACCOUNT_ID}, SECRET_KEY {SECRET_KEY}")
    Configuration.account_id = ACCOUNT_ID
    Configuration.secret_key = SECRET_KEY

    payment = Payment.create(
        {"amount": {"value": 2200.00, "currency": "RUB"}, "capture": True,
         "confirmation": {"type": "redirect", "return_url": "https://t.me/teeest_paaay_bot"},
         "description": "Расширенная гарантия 3 года",
         "metadata": {'order_number': '1'},
         "receipt": {"customer": {"email": "zh.vitaliy92@yandex.ru"},
                     "items": [
                         {
                             "description": "Расширенная гарантия 2 года ",  # Название товара
                             "quantity": "1",
                             "amount": {"value": 2200.00, "currency": "RUB"},  # Сумма и валюта
                             "vat_code": "1"}]}})

    payment_data = json.loads(payment.json())
    payment_id = payment_data['id']
    payment_url = (payment_data['confirmation'])['confirmation_url']
    logger.info(f"Ссылка для оплаты: {payment_url}, ID оплаты {payment_id}")
    return payment_url, payment_id

def register_payment_handlers():
    """Регистрация обработчиков для бота"""
    dp.message.register(extended_warranty_2_years_handlers)
    dp.message.register(extended_warranty_3_years_handlers)
