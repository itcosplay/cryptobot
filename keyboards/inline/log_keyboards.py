from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def create_kb_under_log():
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add (
        InlineKeyboardButton (
            text='вернуться к заявке',
            callback_data='back_to_request'
        )
    )

    keyboard.add (
        InlineKeyboardButton (
            text=f'главное меню',
            callback_data='back_to_main_menu'
        )
    )

    return keyboard

