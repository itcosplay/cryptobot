from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from data import sticker
from loader import dp
from loader import bot
from loader import permit
from loader import sheet
from states import Processing
from keyboards import create_kb_coustom_main_menu
from utils import notify_about_permit_to_order
from utils import updating_log


@dp.message_handler(state=Processing.add_permit)
async def add_permit_data(message:Message, state:FSMContext):
    data_state = await state.get_data()

    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['message_to_delete']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    request = data_state['chosen_request']
    permit_id = request[1]
    request_numb = request[2]
    permit_date = request[0]
    old_permit_text = permit.get_old_permit_text_or_empty(permit_id)

    if old_permit_text == 'данных нет...':
        new_permit_text = message.text
        
    else:
        new_permit_text = old_permit_text + ', ' + message.text
    
    username = message.chat.username

    user = message.chat.username
    request[9] = updating_log (
        'PERMIT',
        user,
        request,
        update_data='Добавлен пропуск'
    )

    try:
        result = await message.answer_sticker (
            sticker['go_to_table']
        )
        permit.clear_table()
        permit.write_new_permit (
            permit_id,
            request_numb,
            permit_date,
            permit_text=new_permit_text
        )
        sheet.replace_row(request)

    except Exception:
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=result.message_id
        )
        await message.answer_sticker (
            sticker['not_connection']
        )
        await message.answer (
            text='Не удалось соединиться с гугл таблицей',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )

        return

    await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)

    await notify_about_permit_to_order(request_numb, username)

    await message.answer (
        text='Новый пропуск добавлен, секретарь оповещен!',
        reply_markup=create_kb_coustom_main_menu(message.from_user.id)
    )
    await state.finish()
    # ---> main_menu <---

