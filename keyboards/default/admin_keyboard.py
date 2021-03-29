from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



def create_kb_coustom_main_menu(user_id):
    from loader import db
    from data.config import super_admins

    if not user_id in super_admins:
        user_status = db.get_user_status(id=user_id)
    else:
        user_status = 'admin'

    keyboard = ReplyKeyboardMarkup()

    if user_status == 'admin':
        keyboard.add(KeyboardButton(text='права пользователей'))
        keyboard.insert(KeyboardButton(text='информация о смс'))

        keyboard.add(KeyboardButton(text='создать заявку'))
        keyboard.insert(KeyboardButton(text='в работе'))

        keyboard.add(KeyboardButton(text='пропуска'))
        keyboard.insert(KeyboardButton(text='создать пропуск'))

    elif user_status == 'secretary':
        keyboard.add(KeyboardButton(text='информация о смс'))
        keyboard.add(KeyboardButton(text='пропуска'))
        
    else:
        keyboard.add(KeyboardButton(text='права пользователей'))
        keyboard.insert(KeyboardButton(text='информация о смс'))

        keyboard.add(KeyboardButton(text='создать заявку'))
        keyboard.insert(KeyboardButton(text='в работе'))

        keyboard.add(KeyboardButton(text='пропуска'))

    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True

    return keyboard



main_menu = ReplyKeyboardMarkup (

    keyboard = [
        [
            KeyboardButton(text='права пользователей'),
            KeyboardButton(text='информация о смс')
        ],
        [
            KeyboardButton(text='создать заявку'),
            KeyboardButton(text='в работе')
        ],
        [
            KeyboardButton(text='пропуска'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)