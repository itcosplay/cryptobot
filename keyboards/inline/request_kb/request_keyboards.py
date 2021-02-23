from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_kb_request_from():
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'чейндж',
            callback_data = 'changer'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'оператор',
            callback_data = 'operator'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'отмена',
            callback_data = 'exit'
        )
    )

    return keyboard


def create_kp_operation_type():
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'прием',
            callback_data = 'recive'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'выдача',
            callback_data = 'takeout'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'доставка',
            callback_data = 'delivery'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'кэшин',
            callback_data = 'cache_in'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'обмен',
            callback_data = 'change'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'снятие с карт',
            callback_data = 'cache_atm'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'отмена',
            callback_data = 'exit'
        )
    )

    return keyboard

def create_kb_choose_currency():
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'рубли',
            callback_data = 'rub'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'доллары',
            callback_data = 'usd'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'евро',
            callback_data = 'eur'
        )
    )

    return keyboard
    