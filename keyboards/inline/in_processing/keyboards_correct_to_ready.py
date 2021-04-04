from data import all_emoji

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData


cb_corrected_sum = CallbackData('cb_cors', 'type_btn')
def create_kb_corrected_sum():
    emo_snail = all_emoji['back__main_menu']
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