# команда меню "права пользователей"

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command

from filters.IsAdmin import IsAdmin
from loader import dp, db

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



@dp.message_handler(IsAdmin(), text='права пользователей')
async def rights_users(message:Message):
    from keyboards.inline.group_users_buttons import group_users_buttons

    await message.reply('текущие группы с пользователями:', reply_markup=group_users_buttons)


@dp.callback_query_handler(lambda c: c.data == 'admin')
async def get_admins(call:CallbackQuery):
    await call.answer()

    text = 'Вы выбрали всех администраторов'
    
    from keyboards.inline.group_users_buttons import admin_users

    await call.message.answer(text, reply_markup=admin_users)


@dp.callback_query_handler(lambda c: c.message.text == 'Вы выбрали всех администраторов')
async def change_status(call:CallbackQuery):
    await call.answer()

    user_change_status_id = call.data

    await call.message.answer(f'Изменить стату для {user_change_status_id}')
