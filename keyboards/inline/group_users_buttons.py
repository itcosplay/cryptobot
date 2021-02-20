from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db
from keyboards.inline.callback_data import change_button_data
from keyboards.inline.callback_data import group_users_data

def create_kb_groups_users():
    print('function: create_kb_groups_users')
    current_statuses = db.get_all_statuses()

    all_statuses = {
        'admin': 'администраторы',
        'changer': 'чейнджи',
        'operator': 'операторы',
        'secretary': 'секретари',
        'executor': 'исполнители',
        'permit': 'на пропуск',
        'request': 'в статусе "запрос"',
        'block': 'заблокированны'
    }

    kb_groups_users = InlineKeyboardMarkup()

    for status in current_statuses:
        if status in all_statuses.keys():
            text = all_statuses[status]
        else:
            text = 'Тут какая-то хуйня...'

        kb_groups_users.add (
            InlineKeyboardButton (
                text = text,
                callback_data = group_users_data.new (
                    group = status,
                    handler = 'statuses'
                )
            )
        )

    return kb_groups_users



# admin_users = InlineKeyboardMarkup()
# admin_users_list = db.select_user(status='admin')

# for user in admin_users_list:
#     admin_users.add (
#         InlineKeyboardButton(text=user[1], callback_data=user[1])
#     )
#     admin_users.insert (
#         InlineKeyboardButton (
#             text = 'изменить',
#             callback_data = change_button_data.new (
#                 user_id = user[0],
#                 user_name = user[1],
#                 user_status = user[2],
#                 type_button = 'change_button'
#             )
#         )
#     )