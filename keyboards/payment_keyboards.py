from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger


def back_to_main_menu_keyboard_garan():
    try:
        rows = [
            [InlineKeyboardButton(text='🧾 Расширенная гарантия 2 года - 1300 руб.',
                                  callback_data='extended_warranty_2_years')],
            [InlineKeyboardButton(text='🧾 Расширенная гарантия 3 года - 2200 руб.',
                                  callback_data='extended_warranty_3_years')],
            [InlineKeyboardButton(text='🔙 Назад в меню', callback_data='back_to_menu')]
        ]
        check_the_warranty_card_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
        return check_the_warranty_card_keyboards
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def extended_warranty_2_years_continue_keyboard(url, id_pay):
    """
    Клавиатура для продолжения оплаты
    :param url: url для перехода на страницу оплаты
    :param id_pay: id оплаты (проверка оплаты)
    """
    try:
        rows = [
            [
                InlineKeyboardButton(text='Продолжить', url=url),
                InlineKeyboardButton(text='Проверить оплату', callback_data=f"two_years_{id_pay}"),
            ],
            [InlineKeyboardButton(text='🔙 Назад в меню', callback_data='back_to_menu')]
        ]
        check_the_warranty_card_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
        return check_the_warranty_card_keyboards
    except Exception as e:
        logger.error(f"Ошибка: {e}")


if __name__ == '__main__':
    back_to_main_menu_keyboard_garan()
