from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData


cb_what_sum = CallbackData('cb_ws', 'type_btn')


def create_kb_what_sum(request):
    if not request[5] == '-': sum_RUB = request[5] + ' RUB;'
    else: sum_RUB = ''

    if not request[6] == '-': sum_USD = request[6] + ' USD;'
    else: sum_USD =''

    if not request[7] == '-': sum_EUR = request[7] + ' EUR;'
    else: sum_EUR = ''

    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'с текущей ({} {} {})'.format(sum_RUB, sum_USD, sum_EUR),
            callback_data = cb_what_sum.new(type_btn='with_current')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'корректировать',
            callback_data = cb_what_sum.new(type_btn='with_another')
        )
    )

    return keyboard


cb_choose_currency = CallbackData('cbkbws', 'curr', 'type_btn')


def create_kb_choose_currency(request):
    if not request[5] == '-': sum_RUB = request[5] + ' RUB'
    else: sum_RUB = ''

    if not request[6] == '-': sum_USD = request[6] + ' USD'
    else: sum_USD =''

    if not request[7] == '-': sum_EUR = request[7] + ' EUR'
    else: sum_EUR = ''

    keyboard = InlineKeyboardMarkup()

    if not request[5] == '-':
        keyboard.add (
            InlineKeyboardButton (
                text = '{}'.format(sum_RUB),
                callback_data = cb_choose_currency.new(curr='RUB', type_btn='change_curr')
            )
        )
    
    if not request[6] == '-':
        keyboard.add (
            InlineKeyboardButton (
                text = '{}'.format(sum_USD),
                callback_data = cb_choose_currency.new(curr='USD', type_btn='change_curr')
            )
        )

    if not request[7] == '-':
        keyboard.add (
            InlineKeyboardButton (
                text = '{}'.format(sum_EUR),
                callback_data = cb_choose_currency.new(curr='EUR', type_btn='change_curr')
            )
        )
    
    return keyboard