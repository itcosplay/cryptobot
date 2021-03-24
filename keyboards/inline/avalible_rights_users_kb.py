from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db
from keyboards.inline.callback_data import set_status_data

def create_kb_change_status_handler(user_data):
    print('create_kb_change_status_handler(user_data)')
    user_status = db.get_user_status(id=user_data['user_id'])

    list_rights = {
        'admin': 'администратор',
        'changer': 'чейндж',
        'operator': 'оператор',
        'secretary': 'секретарь',
        'executor': 'исполнитель',
        'permit': 'на пропуск',
        'request': 'в статус "запрос"',
        'block': 'заблокировать',
        'delete': 'удалить'
    }

    avalible_rights_users_kb = InlineKeyboardMarkup()

    for status in list_rights.keys():
        if user_status != status:
            avalible_rights_users_kb.add (
                InlineKeyboardButton (
                    text = list_rights[status],
                    callback_data = set_status_data.new (
                        id = user_data['user_id'],
                        # user_name = user_data['user_name'],
                        new_st = status,
                        type_btn = 'set_st_btn'
                    )
                )
            )

    return avalible_rights_users_kb

