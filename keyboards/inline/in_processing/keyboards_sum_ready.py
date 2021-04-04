
from emoji import emojize

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import all_emoji

from utils.googlesheets import send_to_google
from utils.set_minus_and_plus_currences import set_minus_and_plus
from utils.get_minuses_sum_FGH import get_minus_FGH



cb_what_sum = CallbackData('cb_ws', 'type_btn')
def create_kb_what_sum():
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'скорректировать',
            callback_data = cb_what_sum.new(type_btn='correct_sum')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'подтвердить',
            callback_data = cb_what_sum.new(type_btn='confirm_sum')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'вернуться к заявке',
            callback_data = cb_what_sum.new(type_btn='back_to_chosen_request')
        )
    )
    back__main_menu = all_emoji['back__main_menu']
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
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
        if not request[5] == '0':
            rub = request[5]
            rub = str(rub)
            if rub[0] != '-': rub = '+' + rub + ' ₽'
            else: rub = rub + ' ₽'
        else: rub = ''

        if not request[6] == '0':
            usd = request[6]
            usd = str(usd)
            if usd[0] != '-': usd = '+' + usd + ' $'
            else: usd = usd + ' $'
        else: usd = ''

        if not request[7] == '0':
            eur = request[7]
            eur = str(eur)
            if eur[0] != '-': eur = '+' + eur + ' €'
            else: eur = eur + ' €'
        else: eur = ''

    else:
        if not request[5] == '0':
            rub = request[5]
            rub = str(rub)
            if rub[0] == '-': rub = rub[1:] + ' ₽'
            else: rub = rub + ' ₽'
        else: rub = ''

        if not request[6] == '0':
            usd = request[6]
            usd = str(usd)
            if usd[0] == '-': usd = usd[1:] + ' $'
            else: usd = usd + ' $'
        else: usd = ''

        if not request[7] == '0':
            eur = request[7]
            eur = str(eur)
            if eur[0] == '-': eur = eur[1:] + ' €'
            else: eur = eur + ' €'
        else: eur = ''

    keyboard = InlineKeyboardMarkup()

    if not request[5] == '0':
        keyboard.add (
            InlineKeyboardButton (
                text = '{}'.format(rub),
                callback_data = cb_choose_currency.new(curr='rub', type_btn='change_curr')
            )
        )
    
    if not request[6] == '0':
        keyboard.add (
            InlineKeyboardButton (
                text = '{}'.format(usd),
                callback_data = cb_choose_currency.new(curr='usd', type_btn='change_curr')
            )
        )

    if not request[7] == '0':
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



cb_what_sum_correct = CallbackData('cbwsc', 'curr', 'type_btn')
def create_kb_what_sum_correct(request):
    
    keyboard = InlineKeyboardMarkup()

    rub, usd, eur = get_minus_FGH(request)

    if rub != '':
        keyboard.add (
            InlineKeyboardButton (
                text=rub,
                callback_data = cb_what_sum_correct.new (
                    curr='rub',
                    type_btn='change_curr'
                )
            )
        )

    if usd != '':
        keyboard.add (
            InlineKeyboardButton (
                text=usd,
                callback_data = cb_what_sum_correct.new (
                    curr='usd',
                    type_btn='change_curr'
                )
            )
        )

    if eur != '':
        keyboard.add (
            InlineKeyboardButton (
                text=eur,
                callback_data = cb_what_sum_correct.new (
                    curr='eur',
                    type_btn='change_curr'
                )
            )
        )

    emo_snail = emojize(':snail:', use_aliases=True)
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {emo_snail} главное меню',
            callback_data=cb_what_sum_correct.new (
                curr='-',
                type_btn='back_main_menu'
            )
        )
    )

    return keyboard