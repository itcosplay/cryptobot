from emoji import emojize

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData


cb_confirm = CallbackData('cb_cm', 'type_btn')


def create_kb_confirm():
    emo_snail = emojize(':snail:', use_aliases=True)
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'подтверждаю!',
            callback_data = cb_confirm.new(type_btn='CONFIRM')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'вернуться к заявке',
            callback_data = cb_confirm.new(type_btn='BACK')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = f'назад {emo_snail} главное меню',
            callback_data = cb_confirm.new(type_btn='exit')
        )
    )

    return keyboard
