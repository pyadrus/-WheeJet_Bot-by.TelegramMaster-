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


if __name__ == '__main__':
    greeting_keyboard()
