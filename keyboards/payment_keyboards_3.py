from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

def extended_warranty_3_years_continue_keyboard(url, id_pay):
    """
        Клавиатура для продолжения оплаты
        :param url: url для перехода на страницу оплаты
        :param id_pay: id оплаты (проверка оплаты)
        """
    try:
        rows = [
            [
                InlineKeyboardButton(text='Продолжить', url=url),
                InlineKeyboardButton(text='Проверить оплату', callback_data=f"three_years_{id_pay}"),
            ],
            [InlineKeyboardButton(text='🔙 Назад в меню', callback_data='back_to_menu')]
        ]
        check_the_warranty_card_keyboar = InlineKeyboardMarkup(inline_keyboard=rows)
        return check_the_warranty_card_keyboar
    except Exception as e:
        logger.error(f"Ошибка: {e}")
