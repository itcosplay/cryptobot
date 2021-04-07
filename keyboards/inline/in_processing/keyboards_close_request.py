from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import all_emoji


cb_confirm_close_request = CallbackData('cb_ccr', 'type_btn')
def create_kb_confirm_close_request(request):
    emo_snail = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()

    keyboard.add (
        InlineKeyboardButton (
            text = 'подтверждаю!',
            callback_data = cb_confirm_close_request.new(type_btn='confirm_close')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'закрыть с другой суммой',
            callback_data = cb_confirm_close_request.new(type_btn='another_sum_close')
        )
    )

    if request[5] != '0':
        keyboard.add (
            InlineKeyboardButton (
                text = 'скорректировать синие',
                callback_data = cb_confirm_close_request.new(type_btn='correct_blue')
            )
        )

    keyboard.add (
        InlineKeyboardButton (
            text = 'вернуться к заявке',
            callback_data = cb_confirm_close_request.new(type_btn='back_to_request')
        )
    )  
    keyboard.add (
        InlineKeyboardButton (
            text = f'назад {emo_snail} главное меню',
            callback_data = cb_confirm_close_request.new(type_btn='back__main_menu')
        )
    )

    return keyboard


cb_which_sum_close = CallbackData('cb_wsc', 'type_btn', 'curr')
def create_kb_which_sum_close(request):
    from utils import get_values_FGH

    emo_snail = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()
    rub, usd, eur = get_values_FGH(request)

    if rub != '':
        keyboard.add (
            InlineKeyboardButton (
                text=rub,
                callback_data = cb_which_sum_close.new (
                    curr='rub',
                    type_btn='change_curr'
                )
            )
        )

    if usd != '':
        keyboard.add (
            InlineKeyboardButton (
                text=usd,
                callback_data = cb_which_sum_close.new (
                    curr='usd',
                    type_btn='change_curr'
                )
            )
        )

    if eur != '':
        keyboard.add (
            InlineKeyboardButton (
                text=eur,
                callback_data = cb_which_sum_close.new (
                    curr='eur',
                    type_btn='change_curr'
                )
            )
        )

    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {emo_snail} главное меню',
            callback_data=cb_which_sum_close.new (
                curr='-',
                type_btn='back__main_menu'
            )
        )
    )

    return keyboard