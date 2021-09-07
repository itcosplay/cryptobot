from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_kb_back_button():
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add (
        InlineKeyboardButton (
            text='назад',
            callback_data='back_button'
        )
    )

    return keyboard