from keyboards.inline import request_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from emoji import emojize
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.callback_data import get_info_request_data







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

cb_choose_curr = CallbackData('cbkbws', 'curr', 'type_btn')
def create_kb_choose_curr(rub, usd, eur):
    keyboard = InlineKeyboardMarkup()

    if not rub == '-':
        keyboard.add (
            InlineKeyboardButton (
                text = 'изменить RUB',
                callback_data = cb_choose_curr.new(curr='RUB', type_btn='change_curr')
            )
        )
    
    if not usd == '-':
        keyboard.add (
            InlineKeyboardButton (
                text = 'изменить USD',
                callback_data = cb_choose_curr.new(curr='USD', type_btn='change_curr')
            )
        )

    if not eur == '-':
        keyboard.add (
            InlineKeyboardButton (
                text = 'изменить EUR',
                callback_data = cb_choose_curr.new(curr='EUR', type_btn='change_curr')
            )
        )
    
    return keyboard