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



# cb_choose_curr = CallbackData('cbkbws', 'curr', 'type_btn')
# def create_kb_choose_curr(rub, usd, eur):
#     keyboard = InlineKeyboardMarkup()

#     if not rub == '-':
#         keyboard.add (
#             InlineKeyboardButton (
#                 text = 'изменить RUB',
#                 callback_data = cb_choose_curr.new(curr='RUB', type_btn='change_curr')
#             )
#         )
    
#     if not usd == '-':
#         keyboard.add (
#             InlineKeyboardButton (
#                 text = 'изменить USD',
#                 callback_data = cb_choose_curr.new(curr='USD', type_btn='change_curr')
#             )
#         )

#     if not eur == '-':
#         keyboard.add (
#             InlineKeyboardButton (
#                 text = 'изменить EUR',
#                 callback_data = cb_choose_curr.new(curr='EUR', type_btn='change_curr')
#             )
#         )
    
#     return keyboard