from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger


def greeting_keyboard():
    try:
        rows = [
            [InlineKeyboardButton(text='📞 Связь с поддержкой', url='https://t.me/WheeJet_Sup'), ],
            [InlineKeyboardButton(text='📚 Инструкция', callback_data='instructions'),
             InlineKeyboardButton(text='🛡 Гарантия', callback_data='check_out_the_warranty')],
        ]
        greeting_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
        return greeting_keyboards
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def instructions_keyboard():
    try:
        rows = [
            [InlineKeyboardButton(text='📄 Инструкция',
                                  url='https://docs.google.com/document/d/1miViCx2KmH6PJVXZaaruwbQGleEhbM_gsdZ-uFNhwGY/edit')],
            [InlineKeyboardButton(text='🔍 Проверить / оформить гарантию', callback_data='check_out_the_warranty')],
            [InlineKeyboardButton(text='🔙 Вернуться на главную страницу', callback_data='back_to_menu')],
        ]
        instructions_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
        return instructions_keyboards
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def check_out_the_warranty_keyboard():
    try:
        rows = [
            [InlineKeyboardButton(text='📃 Хочу ознакомится с условиями', url='https://goo.su/Evtaw')],
            [InlineKeyboardButton(text='✅ Хочу заполнить гарантийный талон', callback_data='guarantee_chek')],
            [InlineKeyboardButton(text='🔍 Хочу проверить гарантийный талон', callback_data='check_the_warranty_card')],
            [InlineKeyboardButton(text='🔙 Назад в меню', callback_data='back_to_menu')],
        ]
        check_out_the_warranty_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
        return check_out_the_warranty_keyboards
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def guarantee_chek_keyboard():
    try:
        rows = [
            [InlineKeyboardButton(text='🛒 WILBEREES', callback_data='WILBEREES'),
             InlineKeyboardButton(text='🛒 OZON', callback_data='OZON')],
            [InlineKeyboardButton(text='🏪 Розничный магазин', callback_data='retail_store'),
             InlineKeyboardButton(text='🏫 Выставка', callback_data='Exhibition')],
            [InlineKeyboardButton(text='❓ Другое', callback_data='Other')],
            [InlineKeyboardButton(text='⬅️ Назад', callback_data='check_out_the_warranty')],
        ]
        guarantee_chek_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
        return guarantee_chek_keyboards
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def filled_data_keyboard():
    try:
        rows = [
            [InlineKeyboardButton(text='🧾 Заполнить второй гарантийный талон', callback_data='guarantee_chek')],

            [InlineKeyboardButton(text='🧾 Расширенная гарантия 2 года - 1300 руб.',
                                  callback_data='extended_warranty_2_years')],
            [InlineKeyboardButton(text='🧾 Расширенная гарантия 3 года - 2200 руб.',
                                  callback_data='extended_warranty_3_years')],

            [InlineKeyboardButton(text='🔗 Перейти в канал', url='https://t.me/wheejet_ru')],
            [InlineKeyboardButton(text='⬅️ Вернуться на главную страницу', callback_data='back_to_menu')],
        ]
        filled_data_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
        return filled_data_keyboards
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def back_to_main_menu_keyboard():
    try:
        rows = [
            [InlineKeyboardButton(text='🔙 Назад в меню', callback_data='back_to_menu')]
        ]
        check_the_warranty_card_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
        return check_the_warranty_card_keyboards
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def check_the_warranty_card_keyboard():
    try:
        rows = [
            [InlineKeyboardButton(text='🧾 Скачать гарантийный талон', callback_data='download_warranty_card')],
            [InlineKeyboardButton(text='🔙 Назад в меню', callback_data='back_to_menu')]
        ]
        check_the_warranty_card_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
        return check_the_warranty_card_keyboards
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def contact_details_to_choose_from():
    try:
        rows = [
            [InlineKeyboardButton(text='📞 Телефон (+***)', callback_data='telephone')],
            [InlineKeyboardButton(text='📨 Почта', callback_data='mail')],
            [InlineKeyboardButton(text='🛬 Телеграм (@***)', callback_data='telegram')],
        ]
        contact_details_to_choose_from_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
        return contact_details_to_choose_from_keyboards
    except Exception as e:
        logger.error(f"Ошибка: {e}")


if __name__ == '__main__':
    greeting_keyboard()
    instructions_keyboard()
    check_out_the_warranty_keyboard()
    guarantee_chek_keyboard()
    filled_data_keyboard()
    contact_details_to_choose_from()
    back_to_main_menu_keyboard()
