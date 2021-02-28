from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
            callback_data = 'cashin'
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
            callback_data = 'cash_atm'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'отмена',
            callback_data = 'exit'
        )
    )

    return keyboard


def create_kb_choose_card():
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'альфа',
            callback_data = 'alfa'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'сбер',
            callback_data = 'sber'
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

def create_kb_smart_choose_curr(list):
    keyboard = InlineKeyboardMarkup()
    default_list = {
        'rub': 'рубли', 
        'usd': 'доллары',
        'eur': 'евро'
    }
    for curr_name in default_list.keys():
        if curr_name not in list:
            keyboard.add (
                InlineKeyboardButton (
                    text = default_list[curr_name],
                    callback_data = curr_name
                )
            )

    return keyboard


def create_kb_send_request_atm():
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'отправить',
            callback_data = 'send_btn'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'комментарий',
            callback_data = 'comment'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'заказать пропуск',
            callback_data = 'order_permit'
        )
    )

    keyboard.add (
        InlineKeyboardButton (
            text = 'отменить заявку',
            callback_data = 'exit'
        )
    )

    return keyboard

def create_kb_send_request(currencies):
    keyboard = InlineKeyboardMarkup()
    if len(currencies) < 3:
        keyboard.add (
            InlineKeyboardButton (
                text = 'добавить cумму в другой валюте',
                callback_data = 'add_currency'
            )
        )
    keyboard.add (
        InlineKeyboardButton (
            text = 'отправить',
            callback_data = 'send_btn'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'комментарий',
            callback_data = 'comment'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'заказать пропуск',
            callback_data = 'order_permit'
        )
    )

    keyboard.add (
        InlineKeyboardButton (
            text = 'отменить заявку',
            callback_data = 'exit'
        )
    )

    return keyboard


def create_kb_send_request_for_change(currencies_recive, currencies_give):
    keyboard = InlineKeyboardMarkup()
    if len(currencies_recive) < 3 and len(currencies_give) < 3:
        keyboard.add (
            InlineKeyboardButton (
                text = 'добавить cумму в другой валюте',
                callback_data = 'add_currency'
            )
        )
    keyboard.add (
        InlineKeyboardButton (
            text = 'отправить',
            callback_data = 'send_btn'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'комментарий',
            callback_data = 'comment'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'заказать пропуск',
            callback_data = 'order_permit'
        )
    )

    keyboard.add (
        InlineKeyboardButton (
            text = 'отменить заявку',
            callback_data = 'exit'
        )
    )

    return keyboard

def create_kb_plus_minus():
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = '+',
            callback_data = 'sum_plus'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = '-',
            callback_data = 'sum_minus'
        )
    )

    return keyboard