from emoji import emojize

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

def create_kb_choose_currency_processing(request):
    emo_snail = emojize(':snail:', use_aliases=True)

    if request[3] == 'обмен':
        pass

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