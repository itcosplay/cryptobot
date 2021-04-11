from emoji import emojize
from data import all_emoji

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


cb_confirm_close = CallbackData('cb_cc', 'type_btn')
def create_kb_confirm_close():
    emo_snail = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'подтверждаю!',
            callback_data = cb_confirm_close.new(type_btn='confirm')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'добавить сообщение',
            callback_data = cb_confirm_close.new(type_btn='add_message')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'вернуться к заявке',
            callback_data = cb_confirm_close.new(type_btn='back_to_request')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = f'назад {emo_snail} главное меню',
            callback_data = cb_confirm_close.new(type_btn='back__main_menu')
        )
    )

    return keyboard


def create_kb_confirm_cancel_request():
    emo_snail = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()

    keyboard.add (
        InlineKeyboardButton (
            text = 'отменить заявку',
            callback_data = 'cancel'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'вернуться к заявке',
            callback_data = 'back_to_request'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = f'назад {emo_snail} главное меню',
            callback_data = 'back__main_menu'
        )
    )

    return keyboard
