from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_keyboard():
    rows = [
        [InlineKeyboardButton(text='Редактор текста бота', callback_data='edit_text')],
        [InlineKeyboardButton(text='Получить пользователей запускавших бота', callback_data='get_users_launched_bot')],
    ]
    admin_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
    return admin_keyboards


if __name__ == '__main__':
    admin_keyboard()
