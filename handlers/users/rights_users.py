# команда меню "права пользователей"
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Command

from filters.IsAdmin import IsAdmin
from loader import dp, db

from keyboards.inline.callback_data import change_button_data
from keyboards.inline.callback_data import set_status_data
from keyboards.inline.callback_data import group_users_data


@dp.message_handler(IsAdmin(), text='права пользователей')
async def rights_users(message:Message):
    from keyboards.inline.group_users_buttons import create_kb_groups_users

    kb_groups_users = create_kb_groups_users()

    await message.answer('ТЕКУЩИЕ ГРУППЫ ПОЛЬЗОВАТЕЛЕЙ:', reply_markup=kb_groups_users)


@dp.callback_query_handler(group_users_data.filter(handler='statuses'))
async def get_admins(call:CallbackQuery):
    await call.answer()

    text = 'Администраторы:'
    
    # from keyboards.inline.group_users_buttons import admin_users

    # await call.message.reply(text, reply_markup=admin_users)
    await call.message.reply(text)


# @dp.callback_query_handler(change_button_data.filter(type_button='change_button'))
# async def change_status(call:CallbackQuery):
#     await call.answer()

#     user_data = change_button_data.parse(call.data)
#     # Example of result change_button_data.parse(call.data):
#     # {'@': 'change_button', 'user_id': '1637852195', 'user_name': 'myTestUser', 'type_button': 'change_button'}

#     from keyboards.inline.avalible_rights_users_kb import create_kb_change_status_handler

#     keyboard = create_kb_change_status_handler(user_data)

#     await call.message.answer(f'Выбрать новые права для {user_data["user_name"]}:', reply_markup=keyboard)


# @dp.callback_query_handler(set_status_data.filter(type_button='set_status_btn'))
# async def set_status(call:CallbackQuery):
#     await call.answer()

#     user_data = set_status_data.parse(call.data)
#     # Example of result set_status_data.parse(call.data):
#     # {'@': 'set_status_button', 'user_id': '1637852195', 'user_name': 'myTestUser', 'new_status': 'changer', 'type_button': 'set_status_btn'}

#     db.update_status(user_data['new_status'], user_data['user_id'])

#     await call.message.answer(f'статус установлен')
