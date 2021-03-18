from datetime import datetime

from emoji import emojize

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


cb_current_requests = CallbackData('cb_cr', 'id', 'type_btn')


def create_kb_current_requests(processing_req, ready_req):
    emo_snail = emojize(':snail:', use_aliases=True)
    keyboard = InlineKeyboardMarkup()
    current_date = datetime.today().strftime('%d.%m')

    emo_issuing_office = emojize(':office:', use_aliases=True)    
    emo_cash_recive = emojize(':chart_with_upwards_trend:', use_aliases=True)
    emo_delivery = emojize(':steam_locomotive:', use_aliases=True)
    emo_exchange = emojize(':recycle:', use_aliases=True)
    emo_cash_in = emojize(':atm:', use_aliases=True)
    emo_cash_atm = emojize(':credit_card:', use_aliases=True)
    emo_process = emojize(':hourglass_flowing_sand:', use_aliases=True)
    emo_ready = emojize(':money_with_wings:', use_aliases=True)

    emo_in_chosen_request = {
        'выдача в офисе': emo_issuing_office,
        'прием кэша': emo_cash_recive,
        'доставка': emo_delivery,
        'обмен': emo_exchange,
        'кэшин': emo_cash_in,
        'снятие с карт': emo_cash_atm,

        'В обработке': emo_process,
        'Готово в выдаче': emo_ready
    }

    if len(processing_req) != 0:
        for request in processing_req:
            
            if not current_date == request[0]:
                date_request = '(' + request[0] + ') '
            else:
                date_request = ''

            type_operation = emo_in_chosen_request[request[3]]
            number_request = request[2]
            status_operation = emo_in_chosen_request[request[11]]

            # убираем минусы и при обмене - добавляем плюсы
            if request[3] == 'обмен':
                if not request[5] == '-':
                    rub = request[5]
                    rub = str(rub)
                    if rub[0] == '-': rub = rub + '₽  '
                    else: rub = '+' + rub + '₽  '
                else:
                    rub = ''

                if not request[6] == '-':
                    usd = request[6]
                    usd = str(usd)
                    if usd[0] == '-': usd = usd + '$  '
                    else: usd = '+' + usd + '$  '
                else:
                    usd = ''

                if not request[7] == '-':
                    eur = request[7]
                    eur = str(eur)
                    if eur[0] == '-': eur = eur + '€'
                    else: eur = '+' + eur + '€'
                else:
                    eur = ''

            else:
                if not request[5] == '-':
                    rub = request[5]
                    rub = str(rub)
                    if rub[0] == '-': rub = rub[1:] + '₽  '
                    else: rub = rub + '₽  '
                else: rub = ''

                if not request[6] == '-':
                    usd = request[6]
                    usd = str(usd)
                    if usd[0] == '-': usd = usd[1:] + '$  '
                    else: usd = usd + '$  '
                else: usd = ''

                if not request[7] == '-':
                    eur = request[7]
                    eur = str(eur)
                    if eur[0] == '-': eur = eur[1:] + '€'
                    else: eur = eur + '€'
                else: eur = ''

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

            type_operation = emo_in_chosen_request[request[3]]
            number_request = request[2]
            status_operation = emo_in_chosen_request[request[11]]

            if request[5] != '-': rub = request[5] + '₽  '
            else: rub = ''

            if request[6] != '-': usd = request[6] + '$  '
            else: usd = ''

            if request[7] != '-': eur = request[7] + '€'
            else: eur = ''

            keyboard.add (
                InlineKeyboardButton (
                    text = '{}{} #{} {} {}{}{}'.format(date_request, type_operation, number_request, status_operation, rub, usd, eur),
                    callback_data = cb_current_requests.new (
                        id=number_request,
                        type_btn='get_request'
                    )
                )
            )

    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {emo_snail} главное меню',
            callback_data=cb_current_requests.new (
                id='-',
                type_btn='exit'
            )
        )
    )

    return keyboard