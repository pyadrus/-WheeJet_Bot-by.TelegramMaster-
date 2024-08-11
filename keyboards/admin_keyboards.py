from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_keyboard():
    rows = [
        [InlineKeyboardButton(text='Команды админа', callback_data='admin_commands')],
    ]
    admin_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return admin_keyboards


if __name__ == '__main__':
    admin_keyboard()
