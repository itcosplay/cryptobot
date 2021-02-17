from aiogram import types
from loader import dp

# from data.config import super_admins

# @dp.message_handler(text="меню", user_id=super_admins)
# async def keyboard(message: types.Message):
#     chat_id = message.from_user.id
#     user = types.User.get_current()
#     text = \
#         f'Добро пожаловать, {user.first_name}. ' + \
#         'Используйте команды из меню ниже.'

#     from loader import bot
#     from keyboards.default import admin_keyboard

#     await bot.send_message(chat_id=chat_id, text=text, reply_markup=admin_keyboard.main_menu)


@dp.message_handler()
async def bot_echo(message: types.Message):
    chat_id = message.from_user.id
    text = 'Я тибя не понимать...'

    from loader import bot

    await bot.send_message(chat_id=chat_id, text=text)

