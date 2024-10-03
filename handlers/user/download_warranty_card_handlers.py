import asyncio
import glob
import os

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from aiogram.types import Message
from loguru import logger

from database.database import get_customer_by_warranty_number
from handlers.user.guarantee_chek_handlers import filling_data_hourly_rate, doc2pdf_libreoffice
from keyboards.keyboards import back_to_main_menu_keyboard
from keyboards.keyboards import filled_data_keyboard
from keyboards.payment_keyboards import back_to_main_menu_keyboard_garan
from system.dispatcher import bot, dp, router


def find_file_by_code(path, code):
    # Формируем шаблон имени файла, который будем искать
    file_pattern = '*' + code + '.pdf'
    # Используем функцию glob.glob для поиска всех файлов, соответствующих шаблону
    files = glob.glob(os.path.join(path, file_pattern))
    if len(files) == 0:
        logger.info(f"Файл с кодом {code} не найден.")
        return None
    else:
        logger.info(files[0])  # Выводим первый найденный файл
        return files[0]


class FormeditDownloadWarrantyCard(StatesGroup):
    text_download_warranty_card = State()


@router.callback_query(F.data == "download_warranty_card")
async def download_warranty_card_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.username
    user_first_name = callback_query.from_user.first_name
    user_last_name = callback_query.from_user.last_name
    logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name}")
    text = "Введите номер гарантийного талона который хотите получить"
    await bot.send_message(callback_query.from_user.id,
                           text,
                           disable_web_page_preview=True,
                           parse_mode="HTML"
                           )
    await state.set_state(FormeditDownloadWarrantyCard.text_download_warranty_card)


@router.message(FormeditDownloadWarrantyCard.text_download_warranty_card)
async def phone_number(message: Message, state: FSMContext):
    """Обработчик нажатия на кнопку отправки гарантийного талона, пользователю Telegram бота"""

    contact = message.html_text
    logger.info(contact)
    await state.clear()
    # Пример использования функции
    files = find_file_by_code('completed_form', contact)
    if files is None:
        await message.answer("К сожалению, Ваш гарантийный талон еще не оформлен.", reply_markup=back_to_main_menu_keyboard())

        customer = get_customer_by_warranty_number(warranty_number_value=contact)

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
                                 warranty_number, f'completed_form/Гарантийный_талон_{warranty_number}.docx', '1 год')
        await state.clear()
        doc2pdf_libreoffice(f'completed_form/Гарантийный_талон_{warranty_number}.docx',
                            f'completed_form/Гарантийный_талон_{warranty_number}.pdf')
        await asyncio.sleep(2)
        file = FSInputFile(f'completed_form/Гарантийный_талон_{warranty_number}.pdf')
        await bot.send_document(message.from_user.id, document=file, caption=response_message,
                                parse_mode="HTML", reply_markup=filled_data_keyboard())  # Отправка файла пользователю

    else:
        logger.info(files)  # Выводим первый найденный файл в папке 'completed_form'
        file = FSInputFile(files)
        response_message = f"Гарантийный талон № {contact}"
        await bot.send_document(message.from_user.id, document=file, caption=response_message,
                                parse_mode="HTML", reply_markup=back_to_main_menu_keyboard_garan())  # Отправка файла пользователю


def register_download_warranty_card_handlers():
    """Регистрация обработчиков для бота"""
    dp.message.register(download_warranty_card_handlers)
