from keyboards.inline import request_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_kb_current_requests(list_of_numbs):
    keyboard = InlineKeyboardMarkup()

    for request in list_of_numbs:
        numb = request[0]
        if request[1] != '-': rub = request[1] + 'RUB;'
        else: rub = ''
        if request[2] != '-': usd = request[2] + 'USD;'
        else: usd = ''
        if request[3] != '-': eur = request[3] + 'EUR;'
        else: eur = ''
        keyboard.add (
            InlineKeyboardButton (
                text = '#{};  {}  {}  {}'.format(numb, rub, usd, eur),
                callback_data = numb
            )
        )

    return keyboard
