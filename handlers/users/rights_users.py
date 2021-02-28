# команда меню "права пользователей"
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from filters import IsAdmin
from loader import dp, db, bot

from keyboards.inline.callback_data import change_button_data
from keyboards.inline.callback_data import set_status_data
from keyboards.inline.callback_data import group_users_data


@dp.message_handler(IsAdmin(), text='права пользователей')
async def rights_users(message:Message):
    from keyboards.inline.group_users_buttons import create_kb_groups_users

    kb_groups_users = create_kb_groups_users()

    await message.answer('ГРУППЫ ПОЛЬЗОВАТЕЛЕЙ:', reply_markup=kb_groups_users)


@dp.callback_query_handler(IsAdmin(), group_users_data.filter(handler='statuses'))
async def get_groups(call:CallbackQuery):
    from keyboards.inline.group_users_buttons import create_kb_particular_group
    await call.answer()

    user_data = group_users_data.parse(call.data)
    # Example of result group_users_data.parse(call.data):
    # {'@': 'gud', 'group': 'admin', 'handler': 'statuses'}

    all_statuses = {
        'admin': 'АДМИНИСТРАТОРЫ:',
        'changer': 'ЧЕЙНДЖИ:',
        'operator': 'ОПЕРАТОРЫ:',
        'secretary': 'СЕКРЕТАРИ:',
        'executor': 'ИСПОЛНИТЕЛИ:',
        'permit': 'НА ПРОПУСК:',
        'request': 'В СТАТУСЕ "ЗАПРОС":',
        'block': 'ЗАБЛОКИРОВАННЫ:'
    }

    for status in all_statuses.keys():
        if user_data['group'] == status:
            text = all_statuses[status]
    
    kb_particular_group = create_kb_particular_group(user_data['group'])

    await call.message.answer(text, reply_markup=kb_particular_group)


@dp.callback_query_handler(IsAdmin(), change_button_data.filter(type_button='change_button'))
async def change_status(call:CallbackQuery):
    await call.answer()

    user_data = change_button_data.parse(call.data)
    # Example of result change_button_data.parse(call.data):
    # {'@': 'change_button', 'user_id': '1637852195', 'type_button': 'change_button'}

    from keyboards.inline.avalible_rights_users_kb import create_kb_change_status_handler

    keyboard = create_kb_change_status_handler(user_data)

    print('@dp.callback_query_handler()')
    print('user_name = db.get_user_name(user_data["user_id"])')
    user_name = db.get_user_name(user_data['user_id'])
    await call.message.answer(f'НОВЫЕ ПРАВА для {user_name}:', reply_markup=keyboard)
    # await bot.send_message (
    #     chat_id = call.message.chat.id,
    #     text='введите сумму:'
    # )


@dp.callback_query_handler(IsAdmin(), set_status_data.filter(type_btn='set_st_btn'))
async def set_status(call:CallbackQuery):
    from keyboards.default.admin_keyboard import main_menu
    await call.answer()

    user_data = set_status_data.parse(call.data)
    # Example of result set_status_data.parse(call.data):
    # {'@': 'ssb', 'id': '1637852195', 'new_st': 'admin', 'type_btn': 'set_st_btn'}

    print('callback_query_handler, db.get_user_name')
    user_name = db.get_user_name(user_data['id'])
    
    if user_data['new_st'] == 'delete':
        print('@dp.callback_query_handler(set_status_data.filter(type_button=\'set_status_btn\'))')
        db.delete_user(user_data['id'])

        # await call.answer(f'пользователь {user_data["user_name"]} удален', show_alert=True)
        await call.message.reply(f'пользователь {user_name} УДАЛЕН', reply_markup=main_menu)

    else:
        print('@dp.callback_query_handler(set_status_data.filter(type_button=\'set_status_btn\'))')
        db.update_status(user_data['new_st'], user_data['id'])

        list_rights = {
            'admin': 'администратор',
            'changer': 'чейндж',
            'operator': 'оператор',
            'secretary': 'секретарь',
            'executor': 'исполнитель',
            'permit': 'на пропуск',
            'request': 'в статус "запрос"',
            'block': 'заблокировать',
            'delete': 'удалить'
        }
        # await call.answer(f'статус установлен', show_alert=True)
        await call.message.reply(f'пользователь {user_name} теперь -  {list_rights[user_data["new_st"]].upper()}', reply_markup=main_menu)
        await bot.send_message (
            chat_id = user_data['id'],
            text=f'Ваш запрос обработан. Ваши права - {list_rights[user_data["new_st"]].upper()}'
        )
