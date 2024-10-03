import asyncio
import json
import sqlite3

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from aiogram.types import Message
from loguru import logger
from yookassa import Configuration, Payment

from database.database import get_customer_by_warranty_number
from handlers.user.guarantee_chek_handlers import filling_data_hourly_rate, doc2pdf_libreoffice
from keyboards.keyboards import filled_data_keyboard
from keyboards.payment_keyboards_3 import extended_warranty_3_years_continue_keyboard
from system.dispatcher import bot, dp, router, SECRET_KEY, ACCOUNT_ID, ADMIN_CHAT_ID
from system.working_with_files import load_bot_info


class PaymentYookassa(StatesGroup):
    new_gua = State()


@router.callback_query(F.data == "extended_warranty_3_years")
async def extended_warranty_3_years_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    logger.info(f"{callback_query.from_user.id} {callback_query.from_user.username} "
                f"{callback_query.from_user.first_name} {callback_query.from_user.last_name}")

    urls, payment = payment_yookassa_program_setup_service_3()

    await bot.send_message(callback_query.from_user.id,
                           load_bot_info(messages="messages/extended_warranty.json"),
                           reply_markup=extended_warranty_3_years_continue_keyboard(urls, payment),
                           disable_web_page_preview=True,
                           parse_mode="HTML"
                           )


@dp.callback_query(F.data.startswith("three_years"))
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
                               "Оплата прошла успешно‼️ \n Введите номер гарантийного талона, который был выдан ранее, для актуализации данных\n"
                               "Для возврата в начальное меню, нажмите: /start")
        await state.set_state(PaymentYookassa.new_gua)
    else:
        await bot.send_message(callback_query.message.chat.id, "Payment failed.")


@router.message(PaymentYookassa.new_gua)
async def new_guarantee_chek_3_years_handlers(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений (для админа, чтобы обновить информацию)"""
    text = message.text

    logger.info(text)

    customer = get_customer_by_warranty_number(warranty_number_value=text)

    if customer:

        telegram_id = customer.telegram_id,
        telegram_username = customer.telegram_username,
        product_code = customer.product_code,
        order_number = customer.order_number,
        product_photo = customer.product_photo,
        full_name = customer.full_name,
        contact = customer.contact,
        communication_method = customer.communication_method,
        date_of_purchase = customer.date_of_purchase,
        tipe_shop = customer.tipe_shop,
        warranty_number = customer.warranty_number  # Номер гарантийного талона

        print(f"Найдено: {telegram_id}, {telegram_username}, {product_code}, {order_number}, {product_photo}, {full_name}, {contact}, {communication_method}, {date_of_purchase}, {tipe_shop}, {warranty_number}")
    else:
        print("Запись не найдена.")

    # Отправьте пользователю сообщение со всей собранной информацией
    response_message = (f"🤖 Благодарю за предоставленную Информацию!\n\n"

                        f"Номер гарантийного талона: {text}\n"  # Артикул товара
                        )

    file_dog = f'form/Гарантийный_талон.docx'

    filling_data_hourly_rate(file_dog, product_code[0], full_name[0], date_of_purchase[0], communication_method[0], contact[0],
                             text, f'completed_form/Гарантийный_талон_{text}.docx', '3 года')
    await state.clear()
    doc2pdf_libreoffice(f'completed_form/Гарантийный_талон_{text}.docx',
                        f'completed_form/Гарантийный_талон_{text}.pdf')
    await asyncio.sleep(2)
    file = FSInputFile(f'completed_form/Гарантийный_талон_{text}.pdf')
    await bot.send_document(message.from_user.id, document=file, caption=response_message,
                            parse_mode="HTML", reply_markup=filled_data_keyboard())  # Отправка файла пользователю


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
                             "description": "Расширенная гарантия 3 года ",  # Название товара
                             "quantity": "1",
                             "amount": {"value": 2200.00, "currency": "RUB"},  # Сумма и валюта
                             "vat_code": "1"}]}})

    payment_data = json.loads(payment.json())
    payment_id = payment_data['id']
    payment_url = (payment_data['confirmation'])['confirmation_url']
    logger.info(f"Ссылка для оплаты: {payment_url}, ID оплаты {payment_id}")
    return payment_url, payment_id


def register_payment_handlers_3_years():
    """Регистрация обработчиков для бота"""
    dp.message.register(extended_warranty_3_years_handlers)
    dp.message.register(check_payment_program_setup_service_3)


if __name__ == "__main__":
    payment_yookassa_program_setup_service_3()
    register_payment_handlers_3_years()