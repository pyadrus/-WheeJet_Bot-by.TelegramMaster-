from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def back_to_main_menu_keyboard_garan():
    rows = [
        [InlineKeyboardButton(text='🧾 Расширенная гарантия 2 года - 1300 руб.', callback_data='extended_warranty_2_years')],
        [InlineKeyboardButton(text='🧾 Расширенная гарантия 3 года - 2200 руб.', callback_data='extended_warranty_3_years')],
        [InlineKeyboardButton(text='🔙 Назад в меню', callback_data='back_to_menu')]
    ]
    check_the_warranty_card_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return check_the_warranty_card_keyboards



def extended_warranty_2_years_continue_keyboard(url, id_pay):
    """
    Клавиатура для продолжения оплаты
    :param url: url для перехода на страницу оплаты
    :param id_pay: id оплаты (проверка оплаты)
    """

    rows = [
        [
            InlineKeyboardButton(text='Продолжить', url=url),
            InlineKeyboardButton(text='Проверить оплату', callback_data=f"check_service_{id_pay}"),
        ],
        [InlineKeyboardButton(text='🔙 Назад в меню', callback_data='back_to_menu')]
    ]
    check_the_warranty_card_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return check_the_warranty_card_keyboards


def extended_warranty_3_years_continue_keyboard():
    rows = [
        [InlineKeyboardButton(text='Продолжить', callback_data='extended_warranty_3_years_continue')],
        [InlineKeyboardButton(text='🔙 Назад в меню', callback_data='back_to_menu')]
    ]
    check_the_warranty_card_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return check_the_warranty_card_keyboards



if __name__ == '__main__':
    back_to_main_menu_keyboard_garan()
    extended_warranty_2_years_continue_keyboard()
    extended_warranty_3_years_continue_keyboard()