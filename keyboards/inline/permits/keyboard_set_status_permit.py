from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import all_emoji


cb_set_status_prmt = CallbackData('cb_set_status_prmt', 'type_btn')
def create_kb_set_status_permit():
    keyboard = InlineKeyboardMarkup()

    keyboard.add (
        InlineKeyboardButton (
            text='пропуск заказан',
            callback_data=cb_set_status_prmt.new (
                type_btn='permit_ordered'
            )
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='в офисе',
            callback_data=cb_set_status_prmt.new (
                type_btn='in_office'
            )
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='удалить пропуск',
            callback_data=cb_set_status_prmt.new (
                type_btn='delete_permit'
            )
        )
    )

    back__main_menu = all_emoji['back__main_menu']
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data=cb_set_status_prmt.new (
                type_btn='back__main_menu'
            )
        )
    )

    return keyboard



              