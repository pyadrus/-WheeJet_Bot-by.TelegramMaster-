from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def greeting_keyboard():
    rows = [
        [InlineKeyboardButton(text='💬 Связь с поддержкой', url='https://t.me/WheeJet_Sup'), ],
        [InlineKeyboardButton(text='📖 Инструкция', callback_data='instructions'),
         InlineKeyboardButton(text='🔍 Гарантия', callback_data='check_out_the_warranty')],
        [InlineKeyboardButton(text='🔗 Перейти в канал', url='https://t.me/wheejet_ru')],
    ]
    greeting_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return greeting_keyboards


def instructions_keyboard():
    rows = [
        [InlineKeyboardButton(text='Ссылка на инструкцию',
                              url='https://docs.google.com/document/d/1miViCx2KmH6PJVXZaaruwbQGleEhbM_gsdZ-uFNhwGY/edit')],
        [InlineKeyboardButton(text='Проверить / оформить гарантию', callback_data='check_out_the_warranty')],
        [InlineKeyboardButton(text='Назад в меню', callback_data='back_to_menu')],
    ]
    instructions_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return instructions_keyboards


def check_out_the_warranty_keyboard():
    rows = [
        [InlineKeyboardButton(text='Ссылка на гарантию', callback_data='warranty_link')],
        [InlineKeyboardButton(text='Принимаю условия, заполнить талон', callback_data='guarantee_chek')],
        [InlineKeyboardButton(text='Проверить гарантийный талон', callback_data='check_the_warranty_card')],
        [InlineKeyboardButton(text='Назад в меню', callback_data='back_to_menu')],
    ]
    check_out_the_warranty_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return check_out_the_warranty_keyboards


def guarantee_chek_keyboard():
    rows = [
        [InlineKeyboardButton(text='WILBEREES', callback_data='WILBEREES'),
         InlineKeyboardButton(text='OZON', callback_data='OZON')],
        [InlineKeyboardButton(text='Розничный магазин', callback_data='retail_store'),
         InlineKeyboardButton(text='Выставка', callback_data='Exhibition')],
        [InlineKeyboardButton(text='Другое', callback_data='Other')],
        [InlineKeyboardButton(text='Назад', callback_data='check_out_the_warranty')],
    ]
    guarantee_chek_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return guarantee_chek_keyboards


if __name__ == '__main__':
    greeting_keyboard()
    instructions_keyboard()
    check_out_the_warranty_keyboard()
    guarantee_chek_keyboard()
