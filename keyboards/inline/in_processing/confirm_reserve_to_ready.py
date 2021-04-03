from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import all_emoji


cb_confirm_reserve = CallbackData('cb_confirm_reserve', 'type_btn')
def create_kb_confirm_reserve():
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'подтвердить',
            callback_data = cb_confirm_reserve.new(type_btn='confirm')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'вернуться к заявке',
            callback_data = cb_confirm_reserve.new(type_btn='back_to_request')
        )
    )
    back__main_menu = all_emoji['back__main_menu']
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data=cb_confirm_reserve.new (
                type_btn='back_main_menu'
            )
        )
    )

    return keyboard