# команда меню "права пользователей"

from aiogram import types

from filters.IsAdmin import IsAdmin
from loader import dp, db, bot
# from data.config import super_admins


@dp.message_handler(IsAdmin())
async def rights_users(message: types.Message):
    user_id = message.from_user.id

    await bot.send_message(chat_id=user_id, text='hello admin')
