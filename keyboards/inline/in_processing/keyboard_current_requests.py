from emoji import emojize

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


cb_current_requests = CallbackData('cb_cr', 'id', 'type_btn')


def create_kb_current_requests(processing_req, ready_req):
    keyboard = InlineKeyboardMarkup()
    
    emo_process = emojize(':hourglass_flowing_sand:', use_aliases=True)
    emo_ready = emojize(':money_with_wings:', use_aliases=True)

    if len(processing_req) != 0:
        for request in processing_req:
            numb = request[0]
            if request[1] != '-': rub = request[1] + '₽  '
            else: rub = ''
            if request[2] != '-': usd = request[2] + '$  '
            else: usd = ''
            if request[3] != '-': eur = request[3] + '€'
            else: eur = ''
            keyboard.add (
                InlineKeyboardButton (
                    text = '#{} {} {}{}{}'.format(numb, emo_process, rub, usd, eur),
                    callback_data = cb_current_requests.new (
                        id=numb,
                        type_btn='get_request'
                    )
                )
            )

    if len(ready_req) != 0:
        for request in ready_req:
            numb = request[0]
            if request[1] != '-': rub = request[1] + '₽  '
            else: rub = ''
            if request[2] != '-': usd = request[2] + '$  '
            else: usd = ''
            if request[3] != '-': eur = request[3] + '€'
            else: eur = ''
            keyboard.add (
                InlineKeyboardButton (
                    text = '#{} {} {}{}{}'.format(numb, emo_ready, rub, usd, eur),
                    callback_data = cb_current_requests.new (
                        id=numb,
                        type_btn='get_request'
                    )
                )
            )

    keyboard.add (
        InlineKeyboardButton (
            text='назад >> главное меню',
            callback_data=cb_current_requests.new (
                id='-',
                type_btn='exit'
            )
        )
    )

    return keyboard