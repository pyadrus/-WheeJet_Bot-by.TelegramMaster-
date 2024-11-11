from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_keyboard():
    try:
        rows = [
            [InlineKeyboardButton(text='Команды админа', callback_data='admin_commands')],
        ]
        admin_keyboards = InlineKeyboardMarkup(inline_keyboard=rows)
        return admin_keyboards
    except Exception as e:
        logger.error(f"Ошибка: {e}")


if __name__ == '__main__':
    admin_keyboard()
