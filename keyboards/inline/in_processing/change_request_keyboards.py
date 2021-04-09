from data import all_emoji

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


cb_change_request = CallbackData('cb_mk', 'type_btn')
def create_kb_change_request(request):
    emo_snail = all_emoji['back__main_menu']
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'иная дата',
            callback_data = cb_change_request.new(type_btn='another_data')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'новый номер',
            callback_data = cb_change_request.new(type_btn='new_id')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'переопределить тип',
            callback_data = cb_change_request.new(type_btn='change_type')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'изменить сумму',
            callback_data = cb_change_request.new(type_btn='update_sum')
        )
    )

    if request[5] == '0' or request[6] == '0' or request[7] == '0':
        keyboard.add (
            InlineKeyboardButton (
                text = 'другая валюта',
                callback_data = cb_change_request.new(type_btn='more_currency')
            )
        )

    keyboard.add (
        InlineKeyboardButton (
            text = 'добавить коментарий',
            callback_data = cb_change_request.new(type_btn='add_commetn')
        )
    )

    keyboard.add (
        InlineKeyboardButton (
            text = f'назад {emo_snail} главное меню',
            callback_data = cb_change_request.new(type_btn='back__main_menu')
        )
    )

    return keyboard