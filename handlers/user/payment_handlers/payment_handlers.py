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
from keyboards.payment_keyboards import extended_warranty_2_years_continue_keyboard
from system.dispatcher import bot, dp, router, SECRET_KEY, ACCOUNT_ID, ADMIN_CHAT_ID
from system.working_with_files import load_bot_info


class PaymentYookassaProgramSetupService1Years(StatesGroup):
    new_guarantee_chek_1_years = State()

@router.callback_query(F.data == "extended_warranty_2_years")
async def extended_warranty_2_years_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    try:
        await state.clear()

        user_name = callback_query.from_user.username
        if callback_query.from_user.username is None:
            user_name = ''  # Установим пустую строку вместо None

        logger.info(f"{callback_query.from_user.id} {user_name} "
                    f"{callback_query.from_user.first_name} {callback_query.from_user.last_name}")

        url, payment = payment_yookassa_program_setup_service()

        await bot.send_message(callback_query.from_user.id,
                               load_bot_info(messages="messages/extended_warranty.json"),
                               reply_markup=extended_warranty_2_years_continue_keyboard(url, payment),
                               disable_web_page_preview=True,
                               parse_mode="HTML"
                               )
    except Exception as e:
        logger.error(f"Ошибка: {e}")


@dp.callback_query(F.data.startswith("two_years_2"))
async def check_payment_program_setup_service(callback_query: types.CallbackQuery, state: FSMContext):
    try:
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

            user_name = callback_query.from_user.username
            if callback_query.from_user.username is None:
                user_name = ''  # Установим пустую строку вместо None

            cursor.execute('''INSERT INTO users_pay (user_id, first_name, last_name, username, payment_info, 
                                                          product, date, payment_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (callback_query.from_user.id,
                            callback_query.from_user.first_name,
                            callback_query.from_user.last_name,
                            user_name, payment_info.id, product, date, payment_status))
            conn.commit()

            await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Пользователь:\n"
                                                               f"ID {callback_query.from_user.id},\n"
                                                               f"Username: @{user_name},\n"
                                                               f"Имя: {callback_query.from_user.first_name},\n"
                                                               f"Фамилия: {callback_query.from_user.last_name},\n\n"
                                                               f"Приобрел 'Дополнительную гарантию на 2 года'")

            await bot.send_message(callback_query.from_user.id,
                                   "Оплата прошла успешно‼️ \n Введите номер гарантийного талона, который был выдан ранее, для актуализации данных\n"
                                   "Для возврата в начальное меню, нажмите: /start")
            await state.set_state(PaymentYookassaProgramSetupService1Years.new_guarantee_chek_1_years)
        else:
            await bot.send_message(callback_query.message.chat.id, "Payment failed.")
    except Exception as e:
        logger.error(f"Ошибка: {e}")

@router.message(PaymentYookassaProgramSetupService1Years.new_guarantee_chek_1_years)
async def new_guarantee_chek_1_years_handlers(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений (для админа, чтобы обновить информацию)"""
    try:
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
    
                            f"Номер гарантийного талона: {warranty_number}\n"  # Артикул товара
                            )

        file_dog = f'form/Гарантийный_талон.docx'

        filling_data_hourly_rate(file_dog, product_code[0], full_name[0], date_of_purchase[0], communication_method[0], contact[0],
                                 warranty_number, f'completed_form/Гарантийный_талон_{warranty_number}.docx', '2 года')
        await asyncio.sleep(3)
        await state.clear()
        doc2pdf_libreoffice(f'completed_form/Гарантийный_талон_{warranty_number}.docx',
                            f'completed_form/Гарантийный_талон_{warranty_number}.pdf')
        await asyncio.sleep(2)
        file = FSInputFile(f'completed_form/Гарантийный_талон_{warranty_number}.pdf')
        await bot.send_document(message.from_user.id, document=file, caption=response_message,
                                parse_mode="HTML", reply_markup=filled_data_keyboard())  # Отправка файла пользователю
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def payment_yookassa_program_setup_service():
    """
    Оплата ЮKassa
    карта для тестирования оплаты (2202 4743 0132 2987)
    https://yookassa.ru/developers/payment-acceptance/testing-and-going-live/testing?lang=ru#test-bank-card
    """
    try:
        logger.info(f"ACCOUNT_ID: {ACCOUNT_ID}, SECRET_KEY {SECRET_KEY}")
        Configuration.account_id = ACCOUNT_ID
        Configuration.secret_key = SECRET_KEY

        payment = Payment.create(
            {"amount": {"value": 1300.00, "currency": "RUB"}, "capture": True,
             "confirmation": {"type": "redirect", "return_url": "https://t.me/WheeJet_Bot"},
             "description": "Расширенная гарантия 2 года",
             "metadata": {'order_number': '1'},
             "receipt": {"customer": {"email": "Tim.kylikoff@gmail.com"},
                         "items": [
                             {
                                 "description": "Расширенная гарантия 2 года",  # Название товара
                                 "quantity": "1",
                                 "amount": {"value": 1300.00, "currency": "RUB"},  # Сумма и валюта
                                 "vat_code": "1",
                                 "payment_mode": "full_payment",
                        "payment_subject": "commodity", }]}})

        payment_data = json.loads(payment.json())
        payment_id = payment_data['id']
        payment_url = (payment_data['confirmation'])['confirmation_url']
        logger.info(f"Ссылка для оплаты: {payment_url}, ID оплаты {payment_id}")
        return payment_url, payment_id
    except Exception as e:
        logger.error(f"Ошибка: {e}")




def register_payment_handlers():
    """Регистрация обработчиков для бота"""
    dp.message.register(extended_warranty_2_years_handlers)


if __name__ == "__main__":
    register_payment_handlers()
    payment_yookassa_program_setup_service()
