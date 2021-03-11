from keyboards.inline import request_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from emoji import emojize
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.callback_data import get_info_request_data




def create_kb_current_requests(processing_req, ready_req):
    keyboard = InlineKeyboardMarkup()
    emo_process = emojize(':hourglass_flowing_sand:', use_aliases=True)
    emo_ready = emojize(':money_with_wings:', use_aliases=True)

    if len(processing_req) != 0:
        for request in processing_req:
            numb = request[0]
            if request[1] != '-': rub = request[1] + 'RUB; '
            else: rub = ''
            if request[2] != '-': usd = request[2] + 'USD; '
            else: usd = ''
            if request[3] != '-': eur = request[3] + 'EUR;'
            else: eur = ''
            keyboard.add (
                InlineKeyboardButton (
                    text = '{} #{}; {}{}{}'.format(emo_process, numb, rub, usd, eur),
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


cb_particular = CallbackData('cb', 'type_btn')
def create_kb_for_particular_request():  
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text='отложить на выдачу',
            callback_data=cb_particular.new(type_btn='to_give')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'изменить',
            callback_data=cb_particular.new(type_btn='to_change')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'отменить заявку',
            callback_data=cb_particular.new(type_btn='to_cancel')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'главное меню',
            callback_data=cb_particular.new(type_btn='to_exit')
        )
    )

    return keyboard

cb_what_sum = CallbackData('cbws', 'type_btn')
def create_kb_what_sum():
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'с текущей суммой',
            callback_data = cb_what_sum.new(type_btn='with_current')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'Изменить',
            callback_data = cb_what_sum.new(type_btn='with_another')
        )
    )

    return keyboard


def 