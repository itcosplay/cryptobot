from aiogram import types

from loader import dp, db

ban_list = db.


@dp.message_handler()
async def ban(message: types.Message):
    user_id = message.from_user.id
