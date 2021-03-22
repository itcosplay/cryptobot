from emoji import emojize

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData


cb_what_bluе = CallbackData('cb_wb', 'type_btn')

def create_kb_what_blue():
    emo_snail = emojize(':snail:', use_aliases=True)

    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'без синих',
            callback_data = cb_what_bluе.new(type_btn='without_blue')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'ввести колличество синих',
            callback_data = cb_what_bluе.new(type_btn='enter_blue')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'назад',
            callback_data = cb_what_bluе.new(type_btn='back_to_request')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {emo_snail} главное меню',
            callback_data=cb_what_bluе.new (
                type_btn='back_main_menu'
            )
        )
    )

    return keyboard


cb_confirm_blue = CallbackData('cb_cb', 'type_btn')

def create_kb_confirm_blue():
    emo_snail = emojize(':snail:', use_aliases=True)

    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'подтвердить',
            callback_data = cb_confirm_blue.new(type_btn='confirm')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'назад',
            callback_data = cb_confirm_blue.new(type_btn='back_to_request')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {emo_snail} главное меню',
            callback_data=cb_confirm_blue.new (
                type_btn='back_main_menu'
            )
        )
    )

    return keyboard