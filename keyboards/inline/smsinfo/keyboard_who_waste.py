from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import all_emoji


cb_who_waste = CallbackData('cb_who_waste', 'type_btn')
def create_kb_who_waste():
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text='оператор',
            callback_data=cb_who_waste.new (
                type_btn='Оператор'
            )
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='офис',
            callback_data=cb_who_waste.new (
                type_btn='Офис'
            )
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='Личные Вит',
            callback_data=cb_who_waste.new (
                type_btn='Личные Вит'
            )
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='Личные Кэт',
            callback_data=cb_who_waste.new (
                type_btn='Личные Кэт'
            )
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='ошибка',
            callback_data=cb_who_waste.new (
                type_btn='Ошибка'
            )
        )
    )
    back__main_menu = all_emoji['back__main_menu']
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data=cb_who_waste.new (
                type_btn='back__main_menu'
            )
        )
    )

    return keyboard


cb_yes_no_note = CallbackData('cb_yes_no_note', 'type_btn')
def create_kb_yes_no_note():
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text='да',
            callback_data=cb_yes_no_note.new (
                type_btn='yes'
            )
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='нет',
            callback_data=cb_yes_no_note.new (
                type_btn='no'
            )
        )
    )
    back__main_menu = all_emoji['back__main_menu']
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data=cb_yes_no_note.new (
                type_btn='back__main_menu'
            )
        )
    )

    return keyboard

              