from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

import sqlite3

from loader import dp, db, bot
from data.config import super_admins

from keyboards.default import admin_keyboard
# from loader import bot

@dp.message_handler(CommandStart(), user_id=super_admins)
async def bot_start(message:types.Message):
    user_id = message.from_user.id
    text = 'Здравствуйте, Владыка!'

    await bot.send_message(chat_id=user_id, text=text, reply_markup=admin_keyboard.main_menu)


@dp.message_handler(CommandStart())
async def bot_start(message:types.Message):
    user_id = message.from_user.id
    name = message.from_user.full_name
    print('@dp.message_handler(CommandStart())')
    user_in_db = db.select_user(id=user_id)
    print('============================')
    print(user_in_db)
    print('============================')

    if len(user_in_db) == 0:
        text = f'''
            Здравствуйте, {name}! Ваш запрос в обработке.
        '''

        try:
            db.add_user(id=user_id, name=name)
        except sqlite3.IntegrityError as err:
            print(err)
        
        for admin in super_admins:
            await bot.send_message(chat_id=admin, text=f'поступил новый запрос от {name}')

        await bot.send_message(chat_id=user_id, text=text)

    else:
        status = [item for t in user_in_db for item in t][2]
        list_rights = {
            'admin': {
                'message': 'ваши права  - администратор. Используйте меню.',
                'keyboard': admin_keyboard.main_menu
            },
            'changer': {
                'message': 'ваши права - чейнджер.',
                'keyboard': None
            },
            'operator': {
                'message': 'ваши права - оператор.',
                'keyboard': None
            },
            'secretary': {
                'message': 'ваши права - секретарь.',
                'keyboard': None
            },
            'executor': {
                'message': 'ваши права - исполнитель.',
                'keyboard': None
            },
            'permit': {
                'message': 'вы можете заказать пропуск.',
                'keyboard': None
            },
            'request': {
                'message': 'ваш запрос в обработке.',
                'keyboard': None
            }
        }
        
        for item in list_rights.keys():
            if item == status:
                text = f'{name}, {list_rights[status]["message"]}'
                reply_markup = list_rights[status]['keyboard']

                break

        await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)