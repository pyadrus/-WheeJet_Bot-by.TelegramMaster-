from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from loguru import logger

from database.database import entry_into_the_database_to_fill_out_a_warranty_card
from keyboards.keyboards import guarantee_chek_keyboard, filled_data_keyboard, contact_details_to_choose_from
from system.dispatcher import ADMIN_USER_ID
from system.dispatcher import bot, dp, router
from system.working_with_files import load_bot_info
from system.working_with_files import save_bot_info


class Formedit_guarantee_chek(StatesGroup):
    text_edit_guarantee_chek = State()


@router.message(Command("edit_guarantee_chek"))
async def edit_guarantee_chek(message: Message, state: FSMContext):
    """Обработчик команды /edit_guarantee_chek (Хочу заполнить гарантийный талон)"""
    if message.from_user.id not in ADMIN_USER_ID:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return
    await message.answer("Введите новый текст, используя разметку HTML.")
    await state.set_state(Formedit_guarantee_chek.text_edit_guarantee_chek)


@router.message(Formedit_guarantee_chek.text_edit_guarantee_chek)
async def update_info(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений (для админа, чтобы обновить информацию)"""
    text = message.html_text
    bot_info = text
    save_bot_info(bot_info, file_path="messages/guarantee_chek_messages.json")  # Сохраняем информацию в JSON
    await message.reply("Информация обновлена.")
    await state.clear()


@router.callback_query(F.data == "guarantee_chek")
async def guarantee_chek_handlers(callback_query: types.CallbackQuery) -> None:
    """Заполнение гарантийного талона"""
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.username
    user_first_name = callback_query.from_user.first_name
    user_last_name = callback_query.from_user.last_name
    logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name}")

    await bot.send_message(callback_query.from_user.id,
                           load_bot_info(messages="messages/guarantee_chek_messages.json"),
                           reply_markup=guarantee_chek_keyboard(),
                           disable_web_page_preview=True)


class EnteringCustomerData(StatesGroup):  # Создаем группу состояний
    product_code = State()  # Создаем состояние Артикул товара
    order_number = State()  # Создаем состояние Номер заказа
    product_photo = State()  # Создаем состояние Фото товара
    FULL_NAME = State()  # Создаем состояние ФИО покупателя
    phone_number = State()  # Создаем состояние Телефон покупателя
    mail = State()  # Создаем состояние E-mail покупателя
    telegram = State()  # Создаем состояние Телефон покупателя


@router.callback_query(F.data == "WILBEREES")
async def WILBEREES_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    sign_up_text = "Пожалуйста введите Артикул товара"
    await bot.send_message(callback_query.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.product_code)


@router.callback_query(F.data == "OZON")
async def OZON_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    sign_up_text = "Пожалуйста введите Артикул товара"
    await bot.send_message(callback_query.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.product_code)


@router.callback_query(F.data == "retail_store")
async def retail_store_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    sign_up_text = "Пожалуйста введите Артикул товара"
    await bot.send_message(callback_query.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.product_code)


@router.callback_query(F.data == "Exhibition")
async def Exhibition_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    sign_up_text = "Пожалуйста введите Артикул товара"
    await bot.send_message(callback_query.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.product_code)


@router.callback_query(F.data == "Other")
async def Other_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    sign_up_text = "Пожалуйста введите Артикул товара"
    await bot.send_message(callback_query.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.product_code)


@router.message(EnteringCustomerData.product_code)
async def product_code(message: Message, state: FSMContext):
    text = message.html_text
    logger.info(text)
    await state.update_data(product_code=text)  # Сохранить данные в состояние
    sign_up_text = "Введите номер заказа (чека)"
    await bot.send_message(message.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.order_number)


@router.message(EnteringCustomerData.order_number)
async def order_number(message: Message, state: FSMContext):
    text = message.html_text
    logger.info(text)
    await state.update_data(order_number=text)  # Сохранить данные в состояние
    sign_up_text = "Приложите фото товара"
    await bot.send_message(message.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.product_photo)


@router.message(EnteringCustomerData.product_photo)
async def product_photo(message: Message, state: FSMContext):
    text = message.html_text
    logger.info(text)
    await state.update_data(product_photo=text)  # Сохранить данные в состояние
    sign_up_text = "Введите Ф.И.О."
    await bot.send_message(message.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.FULL_NAME)


@router.message(EnteringCustomerData.FULL_NAME)
async def FULL_NAME(message: Message, state: FSMContext):
    text = message.html_text
    logger.info(text)
    await state.update_data(FULL_NAME=text)  # Сохранить данные в состояние
    sign_up_text = "Введите контактные данные на выбор"
    await bot.send_message(message.from_user.id, sign_up_text, disable_web_page_preview=True,
                           reply_markup=contact_details_to_choose_from())


@router.callback_query(F.data == "telephone")
async def guarantee_chek_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    sign_up_text = "Пожалуйста введите номер телефона"
    await bot.send_message(callback_query.from_user.id, sign_up_text)
    await state.set_state(EnteringCustomerData.phone_number)


@router.callback_query(F.data == "mail")
async def guarantee_chek_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    sign_up_text = "Пожалуйста введите номер email"
    await bot.send_message(callback_query.from_user.id, sign_up_text)
    await state.set_state(EnteringCustomerData.mail)


@router.callback_query(F.data == "telegram")
async def guarantee_chek_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    sign_up_text = "Пожалуйста введите telegram"
    await bot.send_message(callback_query.from_user.id, sign_up_text)
    await state.set_state(EnteringCustomerData.telegram)


@router.message(EnteringCustomerData.phone_number)
async def phone_number(message: Message, state: FSMContext):
    phone_number_text = message.html_text
    logger.info(phone_number_text)
    await state.update_data(phone_number=phone_number_text)  # Сохранить данные в состояние

    # Получить все собранные данные из состояния
    data = await state.get_data()
    product_code = data.get('product_code')
    order_number = data.get('order_number')
    product_photo = data.get('product_photo')
    full_name = data.get('FULL_NAME')
    entry_into_the_database_to_fill_out_a_warranty_card(message.from_user.id, message.from_user.username, product_code,
                                                        order_number, product_photo, full_name, phone_number_text)
    # Отправьте пользователю сообщение со всей собранной информацией
    response_message = (f"Спасибо за предоставленную информацию!\n\n"

                        f"Ваш запрос принят:\n\n"

                        f"Артикул товара: {product_code}\n"
                        f"Номер заказа: {order_number}\n"
                        f"Фото товара: {product_photo}\n"
                        f"Ф.И.О.: {full_name}\n"
                        f"Телефон: {phone_number_text}")
    await state.clear()
    await message.reply(response_message, reply_markup=filled_data_keyboard())


@router.message(EnteringCustomerData.mail)
async def mail(message: Message, state: FSMContext):
    mail = message.html_text
    logger.info(mail)
    await state.update_data(phone_number=mail)  # Сохранить данные в состояние

    # Получить все собранные данные из состояния
    data = await state.get_data()
    product_code = data.get('product_code')
    order_number = data.get('order_number')
    product_photo = data.get('product_photo')
    full_name = data.get('FULL_NAME')
    entry_into_the_database_to_fill_out_a_warranty_card(message.from_user.id, message.from_user.username, product_code,
                                                        order_number, product_photo, full_name, mail)
    # Отправьте пользователю сообщение со всей собранной информацией
    response_message = (f"Спасибо за предоставленную информацию!\n\n"

                        f"Ваш запрос принят:\n\n"

                        f"Артикул товара: {product_code}\n"
                        f"Номер заказа: {order_number}\n"
                        f"Фото товара: {product_photo}\n"
                        f"Ф.И.О.: {full_name}\n"
                        f"Email: {mail}")
    await state.clear()
    await message.reply(response_message, reply_markup=filled_data_keyboard())


@router.message(EnteringCustomerData.telegram)
async def mail(message: Message, state: FSMContext):
    telegram = message.html_text
    logger.info(telegram)
    await state.update_data(phone_number=telegram)  # Сохранить данные в состояние

    # Получить все собранные данные из состояния
    data = await state.get_data()
    product_code = data.get('product_code')
    order_number = data.get('order_number')
    product_photo = data.get('product_photo')
    full_name = data.get('FULL_NAME')
    entry_into_the_database_to_fill_out_a_warranty_card(message.from_user.id, message.from_user.username, product_code,
                                                        order_number, product_photo, full_name, telegram)
    # Отправьте пользователю сообщение со всей собранной информацией
    response_message = (f"Спасибо за предоставленную информацию!\n\n"

                        f"Ваш запрос принят:\n\n"

                        f"Артикул товара: {product_code}\n"
                        f"Номер заказа: {order_number}\n"
                        f"Фото товара: {product_photo}\n"
                        f"Ф.И.О.: {full_name}\n"
                        f"telegram: {telegram}")
    await state.clear()
    await message.reply(response_message, reply_markup=filled_data_keyboard())


def register_guarantee_chek_handlers():
    """Регистрация обработчиков для бота"""
    dp.message.register(guarantee_chek_handlers)
    dp.message.register(WILBEREES_handlers)
    dp.message.register(OZON_handlers)
    dp.message.register(retail_store_handlers)
    dp.message.register(Exhibition_handlers)
    dp.message.register(Other_handlers)
    dp.message.register(edit_guarantee_chek)
