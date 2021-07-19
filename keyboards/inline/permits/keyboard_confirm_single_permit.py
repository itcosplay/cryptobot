from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import all_emoji


def create_kb_confirm_single_permit():
    keyboard = InlineKeyboardMarkup()

    keyboard.add (
        InlineKeyboardButton (
            text='Подтверждаю!',
            callback_data='confirm'
        )
    )
    # keyboard.add (
    #     InlineKeyboardButton (
    #         text='редактировать номер',
    #         callback_data='edit_numb'
    #     )
    # )
    # keyboard.add (
    #     InlineKeyboardButton (
    #         text='редактировать ФИО',
    #         callback_data='edit_full_name'
    #     )
    # )

    back__main_menu = all_emoji['back__main_menu']
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data='back__main_menu'
        )
    )

    return keyboard



              