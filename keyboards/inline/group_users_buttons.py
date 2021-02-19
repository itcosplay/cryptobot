from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db

users_groups = db.get_all_statuses()

list_rights = {
    'admin': 'администраторы',
    'changer': 'чейнджи',
    'operator': 'операторы',
    'secretary': 'секретари',
    'executor': 'исполнители',
    'permit': 'на пропуск',
    'request': 'в статусе "запрос"',
    'block': 'заблокированны'
}

group_users_buttons = InlineKeyboardMarkup()

for group in users_groups:
    if group in list_rights:
        text = list_rights[group]
    else:
        text = group

    group_users_buttons.add(InlineKeyboardButton(text=text, callback_data=group))



admin_users = InlineKeyboardMarkup()

admin_users_list = db.select_user(status='admin')

for user in admin_users_list:
    # admin_users.insert(InlineKeyboardButton(text=user[1], callback_data=user[1]))
    # admin_users.insert(InlineKeyboardButton(text=user[1], callback_data=user[1]))
    admin_users.add(InlineKeyboardButton(text=user[1], callback_data=user[1]))
    admin_users.insert(InlineKeyboardButton(text='изменить', callback_data=user[1]))



# button_1 = InlineKeyboardButton(text='Первая кнопка!', callback_data='button1')



# group_users_buttons = InlineKeyboardMarkup().add(button_1)