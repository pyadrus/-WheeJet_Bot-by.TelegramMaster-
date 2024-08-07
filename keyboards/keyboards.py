from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def greeting_keyboard():
    rows = [
        [InlineKeyboardButton(text='Связь с поддержкой', callback_data='contact_support')],
        [InlineKeyboardButton(text='Инструкция', callback_data='instructions')],
        [InlineKeyboardButton(text='Гарантия', callback_data='guarantee')],
        [InlineKeyboardButton(text='Перейти в канал', callback_data='go_to_channel')],
    ]
    greeting_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return greeting_keyboards


def instructions_keyboard():
    rows = [
        [InlineKeyboardButton(text='Ссылка на инструкцию', callback_data='link_to_instructions')],
        [InlineKeyboardButton(text='Проверить / оформить гарантию', callback_data='check_out_the_warranty')],
        [InlineKeyboardButton(text='Назад в меню', callback_data='back_to_menu')],
    ]
    instructions_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return instructions_keyboards


def check_out_the_warranty__keyboard():
    rows = [
        [InlineKeyboardButton(text='Ссылка на гарантию', callback_data='warranty_link')],
        [InlineKeyboardButton(text='Принимаю условия, заполнить талон', callback_data='i_accept_the_terms_fill_out_the_form')],
        [InlineKeyboardButton(text='Проверить гарантийный талон', callback_data='check_the_warranty_card')],
        [InlineKeyboardButton(text='Назад в меню', callback_data='back_to_menu')],
    ]
    check_out_the_warranty_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return check_out_the_warranty_keyboards


if __name__ == '__main__':
    greeting_keyboard()
    instructions_keyboard()
    check_out_the_warranty__keyboard()
