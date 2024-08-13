from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from loguru import logger
from aiogram.types import FSInputFile
from database.database import entry_into_the_database_to_fill_out_a_warranty_card
from keyboards.keyboards import guarantee_chek_keyboard, filled_data_keyboard, contact_details_to_choose_from
from system.dispatcher import ADMIN_USER_ID
from system.dispatcher import bot, dp, router
from system.working_with_files import load_bot_info
from system.working_with_files import save_bot_info
from docxtpl import DocxTemplate
import uuid


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
    tipe_shop = State()  # Создаем состояние Тип магазина
    date_of_purchase = State()  # Создаем состояние Дата покупки
    communication_method = State()  # Создаем состояние Способ доставки


@router.callback_query(F.data == "WILBEREES")
async def WILBEREES_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    tipe_shop = 'WILBEREES'
    await state.update_data(tipe_shop=tipe_shop)  # Сохраняем тип магазина в состояние
    sign_up_text = "🛒 Введите артикул товара:"
    await bot.send_message(callback_query.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.product_code)


@router.callback_query(F.data == "OZON")
async def OZON_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    tipe_shop = 'OZON'
    await state.update_data(tipe_shop=tipe_shop)  # Сохраняем тип магазина в состояние
    sign_up_text = "🛒 Введите артикул товара:"
    await bot.send_message(callback_query.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.product_code)


@router.callback_query(F.data == "retail_store")
async def retail_store_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    tipe_shop = 'Розничный магазин'
    await state.update_data(tipe_shop=tipe_shop)  # Сохраняем тип магазина в состояние
    sign_up_text = "🛒 Введите артикул товара:"
    await bot.send_message(callback_query.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.product_code)


@router.callback_query(F.data == "Exhibition")
async def Exhibition_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    tipe_shop = 'Выставка'
    await state.update_data(tipe_shop=tipe_shop)  # Сохраняем тип магазина в состояние
    sign_up_text = "🛒 Введите артикул товара:"
    await bot.send_message(callback_query.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.product_code)


@router.callback_query(F.data == "Other")
async def Other_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    sign_up_text = "🛒 Пожалуйста. Введите место покупки:"
    await bot.send_message(callback_query.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.tipe_shop)


@router.message(EnteringCustomerData.tipe_shop)
async def Other_handlers(message: Message, state: FSMContext) -> None:
    custom_shop_type = message.html_text
    await state.update_data(tipe_shop=custom_shop_type)  # Save the custom shop type

    sign_up_text = "🛒 Введите артикул товара:"
    await bot.send_message(message.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.product_code)


@router.message(EnteringCustomerData.product_code)
async def product_code(message: Message, state: FSMContext):
    text = message.html_text
    logger.info(text)
    await state.update_data(product_code=text)  # Сохранить данные в состояние
    sign_up_text = "🛒 Введите номер чека:"
    await bot.send_message(message.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.order_number)


@router.message(EnteringCustomerData.order_number)
async def order_number(message: Message, state: FSMContext):
    text = message.html_text
    logger.info(text)
    await state.update_data(order_number=text)  # Сохранить данные в состояние
    sign_up_text = "🛒 Прикрепите фото товара:"
    await bot.send_message(message.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.product_photo)


@router.message(EnteringCustomerData.product_photo)
async def product_photo(message: Message, state: FSMContext):
    text = message.html_text
    logger.info(text)
    await state.update_data(product_photo=text)  # Сохранить данные в состояние
    sign_up_text = "Введите ваши данные (Ф.И.О.):"
    await bot.send_message(message.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.FULL_NAME)


@router.message(EnteringCustomerData.FULL_NAME)
async def product_photo(message: Message, state: FSMContext):
    text = message.html_text
    logger.info(text)
    await state.update_data(FULL_NAME=text)  # Сохранить данные в состояние
    sign_up_text = "🛒 Введите дату покупки:"
    await bot.send_message(message.from_user.id, sign_up_text, disable_web_page_preview=True)
    await state.set_state(EnteringCustomerData.date_of_purchase)


@router.message(EnteringCustomerData.date_of_purchase)
async def FULL_NAME(message: Message, state: FSMContext):
    text = message.html_text
    logger.info(text)
    await state.update_data(date_of_purchase=text)  # Сохранить данные в состояние
    sign_up_text = "Укажите удобный для Вас способ связи:"
    await bot.send_message(message.from_user.id, sign_up_text, disable_web_page_preview=True,
                           reply_markup=contact_details_to_choose_from())


@router.callback_query(F.data == "telephone")
async def guarantee_chek_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    communication_method = 'Телефон'
    await state.update_data(communication_method=communication_method)  # Сохраняем тип магазина в состояние
    sign_up_text = "Пожалуйста введите номер телефона (+***)"
    await bot.send_message(callback_query.from_user.id, sign_up_text)
    await state.set_state(EnteringCustomerData.phone_number)


@router.callback_query(F.data == "mail")
async def guarantee_chek_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    communication_method = 'Почта'
    await state.update_data(communication_method=communication_method)  # Сохраняем тип магазина в состояние
    sign_up_text = "Пожалуйста введите номер email"
    await bot.send_message(callback_query.from_user.id, sign_up_text)
    await state.set_state(EnteringCustomerData.mail)


@router.callback_query(F.data == "telegram")
async def guarantee_chek_handlers(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    communication_method = 'Телеграм'
    await state.update_data(communication_method=communication_method)  # Сохраняем тип магазина в состояние
    sign_up_text = "Пожалуйста введите telegram (@***)"
    await bot.send_message(callback_query.from_user.id, sign_up_text)
    await state.set_state(EnteringCustomerData.telegram)


@router.message(EnteringCustomerData.phone_number)
async def phone_number(message: Message, state: FSMContext):
    contact = message.html_text
    logger.info(contact)
    await state.update_data(phone_number=contact)  # Сохранить данные в состояние
    # Получить все собранные данные из состояния
    data = await state.get_data()
    product_code = data.get('product_code')
    order_number = data.get('order_number')
    product_photo = data.get('product_photo')
    full_name = data.get('FULL_NAME')
    tipe_shop = data.get('tipe_shop')
    date_of_purchase = data.get('date_of_purchase')
    communication_method = data.get('communication_method')

    # Создание короткого цифрового кода длиной 8 символов
    short_code = str(uuid.uuid4())[:8]
    print(short_code)

    # Отправьте пользователю сообщение со всей собранной информацией
    response_message = (f"🤖 Благодарю за предоставленную Информацию!\n\n"

                        f"Номер гарантийного талона: {short_code}\n"  # Артикул товара
                        )
    warranty_number = short_code
    entry_into_the_database_to_fill_out_a_warranty_card(message.from_user.id, message.from_user.username, product_code,
                                                        order_number, product_photo,
                                                        full_name, contact, communication_method, date_of_purchase,
                                                        tipe_shop, warranty_number)

    file_dog = f'form/Гарантийный_лист.docx'
    warranty_card_number = short_code
    files_dog = f'completed_form/Гарантийный_лист_{short_code}.docx'
    filling_data_hourly_rate(file_dog, product_code, full_name, date_of_purchase, communication_method, contact,
                             warranty_card_number,
                             files_dog)
    await state.clear()
    # await message.reply(response_message, reply_markup=filled_data_keyboard())
    file = FSInputFile(files_dog)
    await bot.send_document(message.from_user.id, document=file, caption=response_message,
                            parse_mode="HTML", reply_markup=filled_data_keyboard())  # Отправка файла пользователю


@router.message(EnteringCustomerData.mail)
async def mail(message: Message, state: FSMContext):
    contact = message.html_text
    logger.info(contact)
    await state.update_data(phone_number=contact)  # Сохранить данные в состояние
    # Получить все собранные данные из состояния
    data = await state.get_data()
    product_code = data.get('product_code')
    order_number = data.get('order_number')
    product_photo = data.get('product_photo')
    full_name = data.get('FULL_NAME')
    tipe_shop = data.get('tipe_shop')
    date_of_purchase = data.get('date_of_purchase')
    communication_method = data.get('communication_method')

    # Создание короткого цифрового кода длиной 8 символов
    short_code = str(uuid.uuid4())[:8]
    print(short_code)

    # Отправьте пользователю сообщение со всей собранной информацией
    response_message = (f"🤖 Благодарю за предоставленную Информацию!\n\n"

                        f"Номер гарантийного талона: {short_code}\n"  # Артикул товара
                        )
    warranty_number = short_code
    entry_into_the_database_to_fill_out_a_warranty_card(message.from_user.id, message.from_user.username, product_code,
                                                        order_number, product_photo,
                                                        full_name, contact, communication_method, date_of_purchase,
                                                        tipe_shop, warranty_number)

    file_dog = f'form/Гарантийный_лист.docx'
    warranty_card_number = short_code
    files_dog = f'completed_form/Гарантийный_лист_{short_code}.docx'
    filling_data_hourly_rate(file_dog, product_code, full_name, date_of_purchase, communication_method, contact,
                             warranty_card_number,
                             files_dog)

    await state.clear()
    file = FSInputFile(files_dog)
    await bot.send_document(message.from_user.id, document=file, caption=response_message,
                            parse_mode="HTML", reply_markup=filled_data_keyboard())  # Отправка файла пользователю


@router.message(EnteringCustomerData.telegram)
async def mail(message: Message, state: FSMContext):
    contact = message.html_text
    logger.info(contact)
    await state.update_data(phone_number=contact)  # Сохранить данные в состояние
    # Получить все собранные данные из состояния
    data = await state.get_data()
    product_code = data.get('product_code')
    order_number = data.get('order_number')
    product_photo = data.get('product_photo')
    full_name = data.get('FULL_NAME')
    tipe_shop = data.get('tipe_shop')
    date_of_purchase = data.get('date_of_purchase')
    communication_method = data.get('communication_method')

    # Создание короткого цифрового кода длиной 8 символов
    short_code = str(uuid.uuid4())[:8]
    print(short_code)

    # Отправьте пользователю сообщение со всей собранной информацией
    response_message = (f"🤖 Благодарю за предоставленную Информацию!\n\n"

                        f"Номер гарантийного талона: {short_code}\n"  # Артикул товара
                        )
    warranty_number = short_code
    entry_into_the_database_to_fill_out_a_warranty_card(message.from_user.id, message.from_user.username, product_code,
                                                        order_number, product_photo, full_name, contact,
                                                        communication_method,
                                                        date_of_purchase, tipe_shop, warranty_number)

    file_dog = f'form/Гарантийный_лист.docx'
    warranty_card_number = short_code
    files_dog = f'completed_form/Гарантийный_лист_{short_code}.docx'
    filling_data_hourly_rate(file_dog, product_code, full_name, date_of_purchase, communication_method, contact, warranty_card_number,
                             files_dog)

    await state.clear()
    file = FSInputFile(files_dog)
    await bot.send_document(message.from_user.id, document=file, caption=response_message,
                            parse_mode="HTML", reply_markup=filled_data_keyboard())  # Отправка файла пользователю


def filling_data_hourly_rate(file_dog, product_code, full_name, date_of_purchase, communication_method, contact,
                             warranty_card_number, files_dog):
    doc = DocxTemplate(file_dog)
    context = {
        'product_code': f"{product_code}",  # Артикул
        'full_name': f"{full_name}",  # Ф.И.О. (Иванов И. И.)
        'date_of_purchase': f"{date_of_purchase}",  # Дата покупки
        'communication_method': f"{communication_method}",  # Способ связи
        'contact': f"{contact}",  # Контакт для связи
        'warranty_card_number': f"{warranty_card_number}",  # Контакт для связи
    }
    doc.render(context)
    doc.save(files_dog)


def register_guarantee_chek_handlers():
    """Регистрация обработчиков для бота"""
    dp.message.register(guarantee_chek_handlers)
    dp.message.register(WILBEREES_handlers)
    dp.message.register(OZON_handlers)
    dp.message.register(retail_store_handlers)
    dp.message.register(Exhibition_handlers)
    dp.message.register(Other_handlers)
    dp.message.register(edit_guarantee_chek)
