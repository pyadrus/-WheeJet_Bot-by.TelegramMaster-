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


if __name__ == '__main__':
    greeting_keyboard()
    instructions_keyboard()
