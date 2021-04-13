import re

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from data import all_emoji
from data import sticker
from keyboards import create_kb_coustom_main_menu
from loader import bot, dp, sheet
from states import Processing
from utils import notify_in_group_chat
from utils import notify_someone


@dp.message_handler(state=Processing.new_request_id)
async def set_date_from_text(message:Message, state:FSMContext):
    data_state = await state.get_data()

    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['message_to_delete']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    chosen_request = data_state['chosen_request']
    old_request_id = chosen_request[2]
    request_type_emoji = all_emoji[chosen_request[3]]
    persone = all_emoji['персона']
    
    match = re.fullmatch(r'\d\d\d\d', message.text)
    
    if match:
        username = message.chat.username
        new_request_id = message.text
        chosen_request[2] = new_request_id
        text = f'{request_type_emoji} #N{old_request_id}\nизменен номер заявки\n{old_request_id} 👉 {new_request_id}\n{persone} @{username}'
        print(chosen_request)
        try:
            result = await message.answer_sticker (
                sticker['go_to_table']
            )
            sheet.update_id_row(old_request_id, new_request_id)

        except Exception as e:
            print(e)
            await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)
            await message.answer_sticker (
                sticker['not_connection']
            )
            await message.answer (
                text='Не удалось соединиться с гугл таблицей',
                reply_markup=create_kb_coustom_main_menu(message.chat.id)
            )

            return

        await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)

        await message.answer (
            text='Дата заявки изменена',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        
        await notify_someone(text, 'admin', 'changer', 'executor')
        await notify_in_group_chat(text)

        await state.finish()
    else:
        result = await message.answer('Неправильный формат номера заявки. Попробуйте еще раз ввести в формате XXXX.\n(Например: 1546)')
        await state.update_data(message_to_delete=result.message_id)
        await Processing.new_request_id.set()
        # to THIS HANDLER