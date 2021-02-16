from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

import sqlite3

from loader import dp, db
# from data.config import super_admins

@dp.message_handler(CommandStart())
async def bot_start(message:types.Message):
    user_id = message.from_user.id

    user_in_db = db.select_user(id=user_id)
    if user_in_db is None:
        print('Такого пользователя еще нет')

    name = message.from_user.full_name

    text = 'Ваш запрос в обработке'

    try:
        db.add_user(id=user_id, name=name)
    except sqlite3.IntegrityError as err:
        print(err)

    from loader import bot

    await bot.send_message(chat_id=user_id, text=text)