from keyboards.inline import request_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from emoji import emojize

from keyboards.inline.callback_data import get_info_request_data

## 'U+1F914'

def create_kb_current_requests(list_of_numbs):
    keyboard = InlineKeyboardMarkup()
    smile = emojize(':thinking face:', use_aliases=True)
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
                text = '{} #{};  {}  {}  {}'.format(smile, numb, rub, usd, eur),
                callback_data = get_info_request_data.new (
                    id=numb,
                    type_btn='GETINFOREQUEST'
                )
            )
        )

    return keyboard
