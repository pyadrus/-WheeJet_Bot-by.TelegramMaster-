from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def greeting_keyboard():
    rows = [
        [InlineKeyboardButton(text='📞 Связь с поддержкой', url='https://t.me/WheeJet_Sup'), ],
        [InlineKeyboardButton(text='📚 Инструкция', callback_data='instructions'),
         InlineKeyboardButton(text='🛡 Гарантия', callback_data='check_out_the_warranty')],
    ]
    greeting_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return greeting_keyboards


def instructions_keyboard():
    rows = [
        [InlineKeyboardButton(text='📄 Инструкция',
                              url='https://docs.google.com/document/d/1miViCx2KmH6PJVXZaaruwbQGleEhbM_gsdZ-uFNhwGY/edit')],
        [InlineKeyboardButton(text='🔍 Проверить / оформить гарантию', callback_data='check_out_the_warranty')],
        [InlineKeyboardButton(text='🔙 Вернуться на главную страницу', callback_data='back_to_menu')],
    ]
    instructions_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return instructions_keyboards


def check_out_the_warranty_keyboard():
    rows = [
        [InlineKeyboardButton(text='📃 Хочу ознакомится с условиями', url='https://goo.su/Evtaw')],
        [InlineKeyboardButton(text='✅ Хочу заполнить гарантийный талон', callback_data='guarantee_chek')],
        [InlineKeyboardButton(text='🔍 Хочу проверить гарантийный талон', callback_data='check_the_warranty_card')],
        [InlineKeyboardButton(text='🔙 Назад в меню', callback_data='back_to_menu')],
    ]
    check_out_the_warranty_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return check_out_the_warranty_keyboards


def guarantee_chek_keyboard():
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


def filled_data_keyboard():
    rows = [
        [InlineKeyboardButton(text='🧾 Заполнить второй гарантийный талон', callback_data='guarantee_chek')],
        [InlineKeyboardButton(text='🔗 Перейти в канал', url='https://t.me/wheejet_ru')],
        [InlineKeyboardButton(text='⬅️ Вернуться на главную страницу', callback_data='back_to_menu')],
    ]
    filled_data_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return filled_data_keyboards


def check_the_warranty_card_keyboard():
    rows = [
        [InlineKeyboardButton(text='🧾 Скачать гарантийный талон', callback_data='download_warranty_card')],
        [InlineKeyboardButton(text='🔙 Назад в меню', callback_data='back_to_menu')]
    ]
    check_the_warranty_card_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return check_the_warranty_card_keyboards


def contact_details_to_choose_from():
    rows = [
        [InlineKeyboardButton(text='📞 Телефон (+***)', callback_data='telephone')],
        [InlineKeyboardButton(text='📨 Почта', callback_data='mail')],
        [InlineKeyboardButton(text='🛬 Телеграм (@***)', callback_data='telegram')],
    ]
    contact_details_to_choose_from_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return contact_details_to_choose_from_keyboards


if __name__ == '__main__':
    greeting_keyboard()
    instructions_keyboard()
    check_out_the_warranty_keyboard()
    guarantee_chek_keyboard()
    filled_data_keyboard()
    contact_details_to_choose_from()
