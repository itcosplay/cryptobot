from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from data.config import super_admins

@dp.message_handler(CommandStart())
async def bot_start(message:types.Message):
    user_id = message.from_user.id
    text = f'Ваш id = {user_id}'

    from loader import bot

    await bot.send_message(chat_id=user_id, text=text)