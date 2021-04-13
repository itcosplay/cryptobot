from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import all_emoji


cb_for_what_waste = CallbackData('cb_for_what_waste', 'type_btn')
def create_kb_for_what_waste(who_waste):
    keyboard = InlineKeyboardMarkup()

    if who_waste == 'Оператор':
        keyboard.add (
            InlineKeyboardButton (
                text='Доставка',
                callback_data=cb_for_what_waste.new (
                    type_btn='Доставка'
                )
            )
        )
        keyboard.add (
            InlineKeyboardButton (
                text='Сотруднику',
                callback_data=cb_for_what_waste.new (
                    type_btn='Сотруднику'
                )
            )
        )
        keyboard.add (
            InlineKeyboardButton (
                text='Не указано',
                callback_data=cb_for_what_waste.new (
                    type_btn='Не указано'
                )
            )
        )
    else:
        keyboard.add (
            InlineKeyboardButton (
                text='Обустройство',
                callback_data=cb_for_what_waste.new (
                    type_btn='Обустройство'
                )
            )
        )
        keyboard.add (
            InlineKeyboardButton (
                text='Еда',
                callback_data=cb_for_what_waste.new (
                    type_btn='Еда'
                )
            )
        )
        keyboard.add (
            InlineKeyboardButton (
                text='Напитки',
                callback_data=cb_for_what_waste.new (
                    type_btn='Напитки'
                )
            )
        )
        keyboard.add (
            InlineKeyboardButton (
                text='Посуда',
                callback_data=cb_for_what_waste.new (
                    type_btn='Посуда'
                )
            )
        )
        keyboard.add (
            InlineKeyboardButton (
                text='Канцтовары',
                callback_data=cb_for_what_waste.new (
                    type_btn='Канцтовары'
                )
            )
        )
        keyboard.add (
            InlineKeyboardButton (
                text='Бытовая химия',
                callback_data=cb_for_what_waste.new (
                    type_btn='Бытовая химия'
                )
            )
        )
        keyboard.add (
            InlineKeyboardButton (
                text='Оплата услуг',
                callback_data=cb_for_what_waste.new (
                    type_btn='Оплата услуг'
                )
            )
        )
    back__main_menu = all_emoji['back__main_menu']
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data=cb_for_what_waste.new (
                type_btn='back__main_menu'
            )
        )
    )

    return keyboard

