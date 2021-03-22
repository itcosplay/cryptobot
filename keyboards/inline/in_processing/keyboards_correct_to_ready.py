from emoji import emojize

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData


cb_corrected_sum = CallbackData('cb_cors', 'type_btn')
def create_kb_corrected_sum():
    emo_snail = emojize(':snail:', use_aliases=True)
    keyboard = InlineKeyboardMarkup()

    keyboard.add (
        InlineKeyboardButton (
            text='подтвердить',
            callback_data = cb_corrected_sum.new (
                type_btn='confirm'
            )
        )
    )

    keyboard.add (
        InlineKeyboardButton (
            text='скорректировать еще сумму',
            callback_data = cb_corrected_sum.new (
                type_btn='correct_else'
            )
        )
    )

    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {emo_snail} главное меню',
            callback_data=cb_corrected_sum.new (
                type_btn='back_main_menu'
            )
        )
    )

    return keyboard