from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from data import all_emoji


def create_kb_reports_menu():
    back__main_menu = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add (
        InlineKeyboardButton (
            text='касса',
            callback_data='box_office'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='суточный отчет',
            callback_data='daily_report'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='недельный отчет',
            callback_data='weekly_report'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='месячный отчет',
            callback_data='monthly_report'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='исполненые сделки',
            callback_data='finished_requests'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data='back__main_menu'
        )
    )

    return keyboard


def create_kb_box_office():
    back__main_menu = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add (
        InlineKeyboardButton (
            text='принять кассу',
            callback_data='recive_box_office'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='сдать кассу',
            callback_data='give_box_office'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data='back__main_menu'
        )
    )

    return keyboard


def create_kb_confirm_box_office():
    back__main_menu = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add (
        InlineKeyboardButton (
            text='Подтвердить!',
            callback_data='confirm_box_office'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='сообщить о проблеме',
            callback_data='raise_problem'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data='back__main_menu'
        )
    )

    return keyboard