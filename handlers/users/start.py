from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

import sqlite3

from loader import dp, db
from data.config import super_admins

@dp.message_handler(CommandStart(), user_id=super_admins)
async def bot_start(message:types.Message):
    user_id = message.from_user.id
    text = 'Здравствуйте, Владыка!'

    from loader import bot
    from keyboards.default import admin_keyboard

    await bot.send_message(chat_id=user_id, text=text, reply_markup=admin_keyboard.main_menu)


@dp.message_handler(CommandStart())
async def bot_start(message:types.Message):
    user_id = message.from_user.id
    name = message.from_user.full_name
    user_in_db = db.select_user(id=user_id)

    from loader import bot

    if user_in_db is None:
        text = f'''
            Здравствуйте, {name}! Ваш запрос в обработке.
        '''

        try:
            db.add_user(id=user_id, name=name)
        except sqlite3.IntegrityError as err:
            print(err)

        await bot.send_message(chat_id=user_id, text=text)

    else:
        status = [item for t in user_in_db for item in t][2]
        list_rights = {
            'admin': 'ваши права  - администратор.',
            'changer': 'ваши права - чейнджер.',
            'operator': 'ваши права - оператор.',
            'secretary': 'ваши права - секретарь.',
            'executor': 'ваши права - исполнитель.',
            'permit': 'вы можете заказать пропуск.',
            'request': 'ваш запрос в обработке.'
        }
        
        for item in list_rights.keys():
            if item == status:
                text = f'{name}, {list_rights[status]}'

                break

        await bot.send_message(chat_id=user_id, text=text)