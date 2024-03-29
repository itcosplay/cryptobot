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
        # keyboard.insert(KeyboardButton(text='информация о смс'))

        keyboard.add(KeyboardButton(text='создать заявку'))
        keyboard.insert(KeyboardButton(text='в работе'))

        keyboard.add(KeyboardButton(text='пропуска'))
        keyboard.insert(KeyboardButton(text='создать пропуск'))

        keyboard.add(KeyboardButton(text='балансы'))
        keyboard.insert(KeyboardButton(text='отчетность'))

    elif user_status == 'changer':
        keyboard.add(KeyboardButton(text='создать заявку'))
        keyboard.insert(KeyboardButton(text='в работе'))
        keyboard.add(KeyboardButton(text='пропуска'))
        keyboard.insert(KeyboardButton(text='создать пропуск'))
        keyboard.add(KeyboardButton(text='балансы'))
        keyboard.insert(KeyboardButton(text='отчетность'))

    elif user_status == 'executor':
        keyboard.add(KeyboardButton(text='в работе'))
        keyboard.add(KeyboardButton(text='балансы'))
        keyboard.add(KeyboardButton(text='отчетность'))

    elif user_status == 'secretary':
        # keyboard.add(KeyboardButton(text='информация о смс'))
        keyboard.add(KeyboardButton(text='пропуска'))
        keyboard.add(KeyboardButton(text='создать пропуск'))
    
    elif user_status == 'permit':
        keyboard.add(KeyboardButton(text='создать пропуск'))
    else:
        pass

    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True

    return keyboard