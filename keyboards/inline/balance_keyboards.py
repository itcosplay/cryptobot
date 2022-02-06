from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from data import all_emoji


def create_kb_what_balance_to_show():
    back__main_menu = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add (
        InlineKeyboardButton (
            text='офис',
            callback_data='office_balance'
        )
    )
    # keyboard.add (
    #     InlineKeyboardButton (
    #         text='карты',
    #         callback_data='cards_balance'
    #     )
    # )
    keyboard.add (
        InlineKeyboardButton (
            text='Кассы 2 и 3',
            callback_data='box_offices_2_3'
        )
    )
    
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data='back__main_menu'
        )
    )

    return keyboard

