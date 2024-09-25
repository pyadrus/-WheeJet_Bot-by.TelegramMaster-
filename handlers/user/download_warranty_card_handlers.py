import glob
import os

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from aiogram.types import Message
from loguru import logger

from keyboards.keyboards import back_to_main_menu_keyboard
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
    else:
        logger.info(files)  # Выводим первый найденный файл в папке 'completed_form'
        file = FSInputFile(files)
        response_message = f"Гарантийный талон № {contact}"
        await bot.send_document(message.from_user.id, document=file, caption=response_message,
                                parse_mode="HTML", reply_markup=back_to_main_menu_keyboard_garan())  # Отправка файла пользователю


def register_download_warranty_card_handlers():
    """Регистрация обработчиков для бота"""
    dp.message.register(download_warranty_card_handlers)
