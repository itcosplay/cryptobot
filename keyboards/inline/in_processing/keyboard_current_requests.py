from datetime import datetime

# from emoji import emojize

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import all_emoji
from utils import set_minus_and_plus_currences

cb_current_requests = CallbackData('cb_cr', 'id', 'type_btn')

def create_kb_current_requests(processing_req, ready_req):
    keyboard = InlineKeyboardMarkup()
    current_date = datetime.today().strftime('%d.%m')

    if len(processing_req) != 0:
        for request in processing_req:

            if not current_date == request[0]:
                date_request = '(' + request[0] + ') '
            else:
                date_request = ''

            type_operation = all_emoji[request[3]]
            number_request = request[2]
            status_operation = all_emoji[request[11]]

            # добавляем плюсы только для отображения
            rub, usd, eur = set_minus_and_plus_currences.set_minus_and_plus(request)
            
            keyboard.add (
                InlineKeyboardButton (
                    text = '{}{} #{} {} {}{}{}'.format(date_request, type_operation, number_request, status_operation, rub, usd, eur),
                    callback_data = cb_current_requests.new (
                        id=number_request,
                        type_btn='get_request'
                    )
                )
            )
            
    if len(ready_req) != 0:
        for request in ready_req:

            if not current_date == request[0]:
                date_request = '(' + request[0] + ') '
            else:
                date_request = ''

            type_operation = all_emoji[request[3]]
            number_request = request[2]
            status_operation = all_emoji[request[11]]

            # добавляем плюсы только для отображения
            rub, usd, eur = set_minus_and_plus_currences.set_minus_and_plus(request)
            
            keyboard.add (
                InlineKeyboardButton (
                    text = '{}{} #{} {} {}{}{}'.format(date_request, type_operation, number_request, status_operation, rub, usd, eur),
                    callback_data = cb_current_requests.new (
                        id=number_request,
                        type_btn='get_request'
                    )
                )
            )
            
    back__main_menu = all_emoji['back__main_menu']
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data=cb_current_requests.new (
                id='-',
                type_btn='exit'
            )
        )
    )

    return keyboard



              