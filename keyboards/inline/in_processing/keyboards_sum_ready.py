import keyboards
import re
from emoji import emojize

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData



cb_what_sum = CallbackData('cb_ws', 'type_btn')
def create_kb_what_sum(request):
    emo_snail = emojize(':snail:', use_aliases=True)

    if request[3] == 'обмен':

        if not request[5] == '-':
            if request[5][0] != '-': rub = ''
            else: rub = request[5] + ' ₽'
        else: rub = ''

        if not request[6] == '-':
            if request[6][0] != '-': usd = ''
            else: usd = request[6] + ' $ '
        else: usd = ''

        if not request[7] == '-':
            if request[7][0] != '-': eur = ''
            else: eur = request[7] + ' €'
        else: eur = ''

    else:

        if not request[5] == '-':
            rub = request[5][1:] + ' ₽'
        else: rub = ''

        if not request[6] == '-':
            usd = ' ' + request[6][1:] + ' $'
        else: usd = ''

        if not request[7] == '-':
            eur = ' ' + request[7][1:] + ' €'
        else: eur = ''

    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'с текущей ({}{}{})'.format(rub, usd, eur),
            callback_data = cb_what_sum.new(type_btn='with_current')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'корректировать',
            callback_data = cb_what_sum.new(type_btn='with_another')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'вернуться к заявке',
            callback_data = cb_what_sum.new(type_btn='BACK')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {emo_snail} главное меню',
            callback_data=cb_what_sum.new (
                type_btn='back_main_menu'
            )
        )
    )

    return keyboard



cb_choose_currency = CallbackData('anprix', 'curr', 'type_btn')
def create_kb_choose_currency_processing(request):
    emo_snail = emojize(':snail:', use_aliases=True)

    # добавляет плюсы и оставляет минусы если операция - обмен
    if request[3] == 'обмен':
        if not request[5] == '-':
            rub = request[5]
            rub = str(rub)
            if rub[0] != '-': rub = '+' + rub + ' ₽'
            else: rub = rub + ' ₽'
        else: rub = ''

        if not request[6] == '-':
            usd = request[6]
            usd = str(usd)
            if usd[0] != '-': usd = '+' + usd + ' $'
            else: usd = usd + ' $'
        else: usd = ''

        if not request[7] == '-':
            eur = request[7]
            eur = str(eur)
            if eur[0] != '-': eur = '+' + eur + ' €'
            else: eur = eur + ' €'
        else: eur = ''

    else:
        if not request[5] == '-':
            rub = request[5]
            rub = str(rub)
            if rub[0] == '-': rub = rub[1:] + ' ₽'
            else: rub = rub + ' ₽'
        else: rub = ''

        if not request[6] == '-':
            usd = request[6]
            usd = str(usd)
            if usd[0] == '-': usd = usd[1:] + ' $'
            else: usd = usd + ' $'
        else: usd = ''

        if not request[7] == '-':
            eur = request[7]
            eur = str(eur)
            if eur[0] == '-': eur = eur[1:] + ' €'
            else: eur = eur + ' €'
        else: eur = ''

    keyboard = InlineKeyboardMarkup()

    if not request[5] == '-':
        keyboard.add (
            InlineKeyboardButton (
                text = '{}'.format(rub),
                callback_data = cb_choose_currency.new(curr='rub', type_btn='change_curr')
            )
        )
    
    if not request[6] == '-':
        keyboard.add (
            InlineKeyboardButton (
                text = '{}'.format(usd),
                callback_data = cb_choose_currency.new(curr='usd', type_btn='change_curr')
            )
        )

    if not request[7] == '-':
        keyboard.add (
            InlineKeyboardButton (
                text = '{}'.format(eur),
                callback_data = cb_choose_currency.new(curr='eur', type_btn='change_curr')
            )
        )

    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {emo_snail} главное меню',
            callback_data=cb_choose_currency.new (
                curr='-',
                type_btn='back_main_menu'
            )
        )
    )
    
    return keyboard



cb_wsc = CallbackData('cbwsc', 'curr', 'type_btn')
def create_kb_what_sum_correct(request):
    emo_snail = emojize(':snail:', use_aliases=True)
    keyboard = InlineKeyboardMarkup()

    if request[5] != '-':
        if request[5][0] == '-':
            rub = request[5][1:]
            keyboard.add (
                InlineKeyboardButton (
                    text=f'{rub} ₽',
                    callback_data = cb_wsc.new (
                        curr='rub',
                        type_btn='change_curr'
                    )
                )
            )

    if request[6] != '-':
        if request[6][0] == '-':
            usd = request[6][1:]
            keyboard.add (
                InlineKeyboardButton (
                    text=f'{usd} $',
                    callback_data = cb_wsc.new (
                        curr='usd',
                        type_btn='change_curr'
                    )
                )
            )

    if request[7] != '-':
        if request[7][0] == '-':
            eur = request[7][1:]
            keyboard.add (
                InlineKeyboardButton (
                    text=f'{eur} €',
                    callback_data = cb_wsc.new (
                        curr='eur',
                        type_btn='change_curr'
                    )
                )
            )
        
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {emo_snail} главное меню',
            callback_data=cb_wsc.new (
                curr='-',
                type_btn='back_main_menu'
            )
        )
    )

    return keyboard