from keyboards.inline import request_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from emoji import emojize

from keyboards.inline.callback_data import get_info_request_data


def create_kb_current_requests(processing_req, ready_req):
    keyboard = InlineKeyboardMarkup()
    emo_process = emojize(':hourglass_flowing_sand:', use_aliases=True)
    emo_ready = emojize(':money_with_wings:', use_aliases=True)

    if len(processing_req) != 0:
        for request in processing_req:
            numb = request[0]
            if request[1] != '-': rub = request[1] + 'RUB;'
            else: rub = ''
            if request[2] != '-': usd = request[2] + 'USD;'
            else: usd = ''
            if request[3] != '-': eur = request[3] + 'EUR;'
            else: eur = ''
            keyboard.add (
                InlineKeyboardButton (
                    text = '{}  #{}; {} {} {}'.format(emo_process, numb, rub, usd, eur),
                    callback_data = get_info_request_data.new (
                        id=numb,
                        type_btn='GETINFOREQUEST'
                    )
                )
            )

    if len(ready_req) != 0:
        for request in ready_req:
            numb = request[0]
            if request[1] != '-': rub = request[1] + 'RUB;'
            else: rub = ''
            if request[2] != '-': usd = request[2] + 'USD;'
            else: usd = ''
            if request[3] != '-': eur = request[3] + 'EUR;'
            else: eur = ''
            keyboard.add (
                InlineKeyboardButton (
                    text = '{}  #{}; {} {} {}'.format(emo_ready, numb, rub, usd, eur),
                    callback_data = get_info_request_data.new (
                        id=numb,
                        type_btn='GETINFOREQUEST'
                    )
                )
            )

    return keyboard
